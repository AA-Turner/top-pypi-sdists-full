# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11lll1111l1_opy_, bstack11ll1llll11_opy_, bstack11lll1111_opy_, bstack111l1llll1_opy_, bstack11l111ll11l_opy_, bstack11l111lll1l_opy_, bstack111llll111l_opy_, bstack1ll1l11l11_opy_, bstack11111ll1l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111111llll1_opy_ import bstack111111ll1ll_opy_
import bstack_utils.bstack11l111lll_opy_ as bstack1l1ll11l11_opy_
from bstack_utils.bstack111ll1l11l_opy_ import bstack1l1111l1_opy_
import bstack_utils.accessibility as bstack1lll11l1_opy_
from bstack_utils.bstack1ll111ll11_opy_ import bstack1ll111ll11_opy_
from bstack_utils.bstack111ll1ll11_opy_ import bstack1111ll1ll1_opy_
bstack1lllll1l1l1l_opy_ = bstack11ll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫῊ")
logger = logging.getLogger(__name__)
class bstack1l1l11ll11_opy_:
    bstack111111llll1_opy_ = None
    bs_config = None
    bstack1lllll111_opy_ = None
    @classmethod
    @bstack111l1llll1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11l1lll1lll_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def launch(cls, bs_config, bstack1lllll111_opy_):
        cls.bs_config = bs_config
        cls.bstack1lllll111_opy_ = bstack1lllll111_opy_
        try:
            cls.bstack1lllll1ll1ll_opy_()
            bstack11ll1ll1l11_opy_ = bstack11lll1111l1_opy_(bs_config)
            bstack11ll1ll1ll1_opy_ = bstack11ll1llll11_opy_(bs_config)
            data = bstack1l1ll11l11_opy_.bstack1llllll11ll1_opy_(bs_config, bstack1lllll111_opy_)
            config = {
                bstack11ll1l1_opy_ (u"ࠬࡧࡵࡵࡪࠪΉ"): (bstack11ll1ll1l11_opy_, bstack11ll1ll1ll1_opy_),
                bstack11ll1l1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧῌ"): cls.default_headers()
            }
            response = bstack11lll1111_opy_(bstack11ll1l1_opy_ (u"ࠧࡑࡑࡖࡘࠬ῍"), cls.request_url(bstack11ll1l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠲࠰ࡤࡸ࡭ࡱࡪࡳࠨ῎")), data, config)
            if response.status_code != 200:
                bstack1l111l1ll1_opy_ = response.json()
                if bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ῏")] == False:
                    cls.bstack1lllll1lll11_opy_(bstack1l111l1ll1_opy_)
                    return
                cls.bstack1llllll11l11_opy_(bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪῐ")])
                cls.bstack1lllll1l11l1_opy_(bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫῑ")])
                return None
            bstack1lllll11lll1_opy_ = cls.bstack1llllll1111l_opy_(response)
            return bstack1lllll11lll1_opy_, response.json()
        except Exception as error:
            logger.error(bstack11ll1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡼࡿࠥῒ").format(str(error)))
            return None
    @classmethod
    @bstack111l1llll1_opy_(class_method=True)
    def stop(cls, bstack1llllll11l1l_opy_=None):
        if not bstack1l1111l1_opy_.on() and not bstack1lll11l1_opy_.on():
            return
        if os.environ.get(bstack11ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪΐ")) == bstack11ll1l1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ῔") or os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭῕")) == bstack11ll1l1_opy_ (u"ࠤࡱࡹࡱࡲࠢῖ"):
            logger.error(bstack11ll1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ῗ"))
            return {
                bstack11ll1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫῘ"): bstack11ll1l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫῙ"),
                bstack11ll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧῚ"): bstack11ll1l1_opy_ (u"ࠧࡕࡱ࡮ࡩࡳ࠵ࡢࡶ࡫࡯ࡨࡎࡊࠠࡪࡵࠣࡹࡳࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡣࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡ࡯࡬࡫࡭ࡺࠠࡩࡣࡹࡩࠥ࡬ࡡࡪ࡮ࡨࡨࠬΊ")
            }
        try:
            cls.bstack111111llll1_opy_.shutdown()
            data = {
                bstack11ll1l1_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭῜"): bstack1ll1l11l11_opy_()
            }
            if not bstack1llllll11l1l_opy_ is None:
                data[bstack11ll1l1_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡲ࡫ࡴࡢࡦࡤࡸࡦ࠭῝")] = [{
                    bstack11ll1l1_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ῞"): bstack11ll1l1_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥࠩ῟"),
                    bstack11ll1l1_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࠬῠ"): bstack1llllll11l1l_opy_
                }]
            config = {
                bstack11ll1l1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧῡ"): cls.default_headers()
            }
            bstack11ll11lll11_opy_ = bstack11ll1l1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨῢ").format(os.environ[bstack11ll1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨΰ")])
            bstack1llllll111ll_opy_ = cls.request_url(bstack11ll11lll11_opy_)
            response = bstack11lll1111_opy_(bstack11ll1l1_opy_ (u"ࠩࡓ࡙࡙࠭ῤ"), bstack1llllll111ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11ll1l1_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤῥ"))
        except Exception as error:
            logger.error(bstack11ll1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࡀࠠࠣῦ") + str(error))
            return {
                bstack11ll1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬῧ"): bstack11ll1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬῨ"),
                bstack11ll1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨῩ"): str(error)
            }
    @classmethod
    @bstack111l1llll1_opy_(class_method=True)
    def bstack1llllll1111l_opy_(cls, response):
        bstack1l111l1ll1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1lllll11lll1_opy_ = {}
        if bstack1l111l1ll1_opy_.get(bstack11ll1l1_opy_ (u"ࠨ࡬ࡺࡸࠬῪ")) is None:
            os.environ[bstack11ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ύ")] = bstack11ll1l1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨῬ")
        else:
            os.environ[bstack11ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ῭")] = bstack1l111l1ll1_opy_.get(bstack11ll1l1_opy_ (u"ࠬࡰࡷࡵࠩ΅"), bstack11ll1l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ`"))
        os.environ[bstack11ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ῰")] = bstack1l111l1ll1_opy_.get(bstack11ll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ῱"), bstack11ll1l1_opy_ (u"ࠩࡱࡹࡱࡲࠧῲ"))
        logger.info(bstack11ll1l1_opy_ (u"ࠪࡘࡪࡹࡴࡩࡷࡥࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨῳ") + os.getenv(bstack11ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩῴ")));
        if bstack1l1111l1_opy_.bstack1lllll1l1111_opy_(cls.bs_config, cls.bstack1lllll111_opy_.get(bstack11ll1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭῵"), bstack11ll1l1_opy_ (u"࠭ࠧῶ"))) is True:
            bstack111111l1l11_opy_, build_hashed_id, bstack1lllll1ll111_opy_ = cls.bstack1lllll1llll1_opy_(bstack1l111l1ll1_opy_)
            if bstack111111l1l11_opy_ != None and build_hashed_id != None:
                bstack1lllll11lll1_opy_[bstack11ll1l1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧῷ")] = {
                    bstack11ll1l1_opy_ (u"ࠨ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠫῸ"): bstack111111l1l11_opy_,
                    bstack11ll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫΌ"): build_hashed_id,
                    bstack11ll1l1_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧῺ"): bstack1lllll1ll111_opy_
                }
            else:
                bstack1lllll11lll1_opy_[bstack11ll1l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫΏ")] = {}
        else:
            bstack1lllll11lll1_opy_[bstack11ll1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬῼ")] = {}
        bstack1lllll11ll1l_opy_, build_hashed_id = cls.bstack1lllll1ll11l_opy_(bstack1l111l1ll1_opy_)
        if bstack1lllll11ll1l_opy_ != None and build_hashed_id != None:
            bstack1lllll11lll1_opy_[bstack11ll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭´")] = {
                bstack11ll1l1_opy_ (u"ࠧࡢࡷࡷ࡬ࡤࡺ࡯࡬ࡧࡱࠫ῾"): bstack1lllll11ll1l_opy_,
                bstack11ll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ῿"): build_hashed_id,
            }
        else:
            bstack1lllll11lll1_opy_[bstack11ll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ ")] = {}
        if bstack1lllll11lll1_opy_[bstack11ll1l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ ")].get(bstack11ll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ ")) != None or bstack1lllll11lll1_opy_[bstack11ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ ")].get(bstack11ll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ ")) != None:
            cls.bstack1llllll11111_opy_(bstack1l111l1ll1_opy_.get(bstack11ll1l1_opy_ (u"ࠧ࡫ࡹࡷࠫ ")), bstack1l111l1ll1_opy_.get(bstack11ll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ ")))
        return bstack1lllll11lll1_opy_
    @classmethod
    def bstack1lllll1llll1_opy_(cls, bstack1l111l1ll1_opy_):
        if bstack1l111l1ll1_opy_.get(bstack11ll1l1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ ")) == None:
            cls.bstack1llllll11l11_opy_()
            return [None, None, None]
        if bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ ")][bstack11ll1l1_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ ")] != True:
            cls.bstack1llllll11l11_opy_(bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ ")])
            return [None, None, None]
        logger.debug(bstack11ll1l1_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ​"))
        os.environ[bstack11ll1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭‌")] = bstack11ll1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭‍")
        if bstack1l111l1ll1_opy_.get(bstack11ll1l1_opy_ (u"ࠩ࡭ࡻࡹ࠭‎")):
            os.environ[bstack11ll1l1_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧ‏")] = json.dumps({
                bstack11ll1l1_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭‐"): bstack11lll1111l1_opy_(cls.bs_config),
                bstack11ll1l1_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧ‑"): bstack11ll1llll11_opy_(cls.bs_config)
            })
        if bstack1l111l1ll1_opy_.get(bstack11ll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ‒")):
            os.environ[bstack11ll1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭–")] = bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ—")]
        if bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ―")].get(bstack11ll1l1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ‖"), {}).get(bstack11ll1l1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ‗")):
            os.environ[bstack11ll1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭‘")] = str(bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭’")][bstack11ll1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ‚")][bstack11ll1l1_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ‛")])
        else:
            os.environ[bstack11ll1l1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ“")] = bstack11ll1l1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ”")
        return [bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠫ࡯ࡽࡴࠨ„")], bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ‟")], os.environ[bstack11ll1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ†")]]
    @classmethod
    def bstack1lllll1ll11l_opy_(cls, bstack1l111l1ll1_opy_):
        if bstack1l111l1ll1_opy_.get(bstack11ll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ‡")) == None:
            cls.bstack1lllll1l11l1_opy_()
            return [None, None]
        if bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ•")][bstack11ll1l1_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ‣")] != True:
            cls.bstack1lllll1l11l1_opy_(bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ․")])
            return [None, None]
        if bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ‥")].get(bstack11ll1l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭…")):
            logger.debug(bstack11ll1l1_opy_ (u"࠭ࡔࡦࡵࡷࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ‧"))
            parsed = json.loads(os.getenv(bstack11ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ "), bstack11ll1l1_opy_ (u"ࠨࡽࢀࠫ ")))
            capabilities = bstack1l1ll11l11_opy_.bstack1lllll1l11ll_opy_(bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ‪")][bstack11ll1l1_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ‫")][bstack11ll1l1_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ‬")], bstack11ll1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ‭"), bstack11ll1l1_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ‮"))
            bstack1lllll11ll1l_opy_ = capabilities[bstack11ll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬ ")]
            os.environ[bstack11ll1l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭‰")] = bstack1lllll11ll1l_opy_
            if bstack11ll1l1_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦ‱") in bstack1l111l1ll1_opy_ and bstack1l111l1ll1_opy_.get(bstack11ll1l1_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤ′")) is None:
                parsed[bstack11ll1l1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ″")] = capabilities[bstack11ll1l1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭‴")]
            os.environ[bstack11ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ‵")] = json.dumps(parsed)
            scripts = bstack1l1ll11l11_opy_.bstack1lllll1l11ll_opy_(bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ‶")][bstack11ll1l1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ‷")][bstack11ll1l1_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ‸")], bstack11ll1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ‹"), bstack11ll1l1_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࠬ›"))
            bstack1ll111ll11_opy_.bstack1lll1lll11_opy_(scripts)
            commands = bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ※")][bstack11ll1l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ‼")][bstack11ll1l1_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࡖࡲ࡛ࡷࡧࡰࠨ‽")].get(bstack11ll1l1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ‾"))
            bstack1ll111ll11_opy_.bstack11lll111l11_opy_(commands)
            bstack11lll11l11l_opy_ = capabilities.get(bstack11ll1l1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ‿"))
            bstack1ll111ll11_opy_.bstack11ll11llll1_opy_(bstack11lll11l11l_opy_)
            bstack1ll111ll11_opy_.store()
        return [bstack1lllll11ll1l_opy_, bstack1l111l1ll1_opy_[bstack11ll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ⁀")]]
    @classmethod
    def bstack1llllll11l11_opy_(cls, response=None):
        os.environ[bstack11ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ⁁")] = bstack11ll1l1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ⁂")
        os.environ[bstack11ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⁃")] = bstack11ll1l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ⁄")
        os.environ[bstack11ll1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧ⁅")] = bstack11ll1l1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ⁆")
        os.environ[bstack11ll1l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ⁇")] = bstack11ll1l1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⁈")
        os.environ[bstack11ll1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭⁉")] = bstack11ll1l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⁊")
        cls.bstack1lllll1lll11_opy_(response, bstack11ll1l1_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢ⁋"))
        return [None, None, None]
    @classmethod
    def bstack1lllll1l11l1_opy_(cls, response=None):
        os.environ[bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭⁌")] = bstack11ll1l1_opy_ (u"ࠩࡱࡹࡱࡲࠧ⁍")
        os.environ[bstack11ll1l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⁎")] = bstack11ll1l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ⁏")
        os.environ[bstack11ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⁐")] = bstack11ll1l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ⁑")
        cls.bstack1lllll1lll11_opy_(response, bstack11ll1l1_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢ⁒"))
        return [None, None, None]
    @classmethod
    def bstack1llllll11111_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⁓")] = jwt
        os.environ[bstack11ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ⁔")] = build_hashed_id
    @classmethod
    def bstack1lllll1lll11_opy_(cls, response=None, product=bstack11ll1l1_opy_ (u"ࠥࠦ⁕")):
        if response == None or response.get(bstack11ll1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫ⁖")) == None:
            logger.error(product + bstack11ll1l1_opy_ (u"ࠧࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠢ⁗"))
            return
        for error in response[bstack11ll1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭⁘")]:
            bstack11l111111l1_opy_ = error[bstack11ll1l1_opy_ (u"ࠧ࡬ࡧࡼࠫ⁙")]
            error_message = error[bstack11ll1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⁚")]
            if error_message:
                if bstack11l111111l1_opy_ == bstack11ll1l1_opy_ (u"ࠤࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠣ⁛"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11ll1l1_opy_ (u"ࠥࡈࡦࡺࡡࠡࡷࡳࡰࡴࡧࡤࠡࡶࡲࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࠦ⁜") + product + bstack11ll1l1_opy_ (u"ࠦࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡪࡵࡦࠢࡷࡳࠥࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤ⁝"))
    @classmethod
    def bstack1lllll1ll1ll_opy_(cls):
        if cls.bstack111111llll1_opy_ is not None:
            return
        cls.bstack111111llll1_opy_ = bstack111111ll1ll_opy_(cls.bstack1lllll1lll1l_opy_)
        cls.bstack111111llll1_opy_.start()
    @classmethod
    def bstack1111llll11_opy_(cls):
        if cls.bstack111111llll1_opy_ is None:
            return
        cls.bstack111111llll1_opy_.shutdown()
    @classmethod
    @bstack111l1llll1_opy_(class_method=True)
    def bstack1lllll1lll1l_opy_(cls, bstack111l11llll_opy_, event_url=bstack11ll1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ⁞")):
        config = {
            bstack11ll1l1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ "): cls.default_headers()
        }
        logger.debug(bstack11ll1l1_opy_ (u"ࠢࡱࡱࡶࡸࡤࡪࡡࡵࡣ࠽ࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡸࡴࠦࡴࡦࡵࡷ࡬ࡺࡨࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࡶࠤࢀࢃࠢ⁠").format(bstack11ll1l1_opy_ (u"ࠨ࠮ࠣࠫ⁡").join([event[bstack11ll1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⁢")] for event in bstack111l11llll_opy_])))
        response = bstack11lll1111_opy_(bstack11ll1l1_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ⁣"), cls.request_url(event_url), bstack111l11llll_opy_, config)
        bstack11ll1ll1l1l_opy_ = response.json()
    @classmethod
    def bstack11ll111ll1_opy_(cls, bstack111l11llll_opy_, event_url=bstack11ll1l1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ⁤")):
        logger.debug(bstack11ll1l1_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡤࡨࡩࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧ⁥").format(bstack111l11llll_opy_[bstack11ll1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⁦")]))
        if not bstack1l1ll11l11_opy_.bstack1lllll1l1ll1_opy_(bstack111l11llll_opy_[bstack11ll1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⁧")]):
            logger.debug(bstack11ll1l1_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡔ࡯ࡵࠢࡤࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨ⁨").format(bstack111l11llll_opy_[bstack11ll1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⁩")]))
            return
        bstack1l1l1ll111_opy_ = bstack1l1ll11l11_opy_.bstack1lllll1l1l11_opy_(bstack111l11llll_opy_[bstack11ll1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⁪")], bstack111l11llll_opy_.get(bstack11ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭⁫")))
        if bstack1l1l1ll111_opy_ != None:
            if bstack111l11llll_opy_.get(bstack11ll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ⁬")) != None:
                bstack111l11llll_opy_[bstack11ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ⁭")][bstack11ll1l1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ⁮")] = bstack1l1l1ll111_opy_
            else:
                bstack111l11llll_opy_[bstack11ll1l1_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭⁯")] = bstack1l1l1ll111_opy_
        if event_url == bstack11ll1l1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨ⁰"):
            cls.bstack1lllll1ll1ll_opy_()
            logger.debug(bstack11ll1l1_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡂࡦࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨⁱ").format(bstack111l11llll_opy_[bstack11ll1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⁲")]))
            cls.bstack111111llll1_opy_.add(bstack111l11llll_opy_)
        elif event_url == bstack11ll1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ⁳"):
            cls.bstack1lllll1lll1l_opy_([bstack111l11llll_opy_], event_url)
    @classmethod
    @bstack111l1llll1_opy_(class_method=True)
    def bstack1ll111l1l1_opy_(cls, logs):
        bstack1llllll11lll_opy_ = []
        for log in logs:
            bstack1lllll1l111l_opy_ = {
                bstack11ll1l1_opy_ (u"࠭࡫ࡪࡰࡧࠫ⁴"): bstack11ll1l1_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩ⁵"),
                bstack11ll1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⁶"): log[bstack11ll1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⁷")],
                bstack11ll1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⁸"): log[bstack11ll1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⁹")],
                bstack11ll1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬ⁺"): {},
                bstack11ll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⁻"): log[bstack11ll1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⁼")],
            }
            if bstack11ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⁽") in log:
                bstack1lllll1l111l_opy_[bstack11ll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⁾")] = log[bstack11ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪⁿ")]
            elif bstack11ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ₀") in log:
                bstack1lllll1l111l_opy_[bstack11ll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ₁")] = log[bstack11ll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭₂")]
            bstack1llllll11lll_opy_.append(bstack1lllll1l111l_opy_)
        cls.bstack11ll111ll1_opy_({
            bstack11ll1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ₃"): bstack11ll1l1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ₄"),
            bstack11ll1l1_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ₅"): bstack1llllll11lll_opy_
        })
    @classmethod
    @bstack111l1llll1_opy_(class_method=True)
    def bstack1lllll1ll1l1_opy_(cls, steps):
        bstack1llllll111l1_opy_ = []
        for step in steps:
            bstack1lllll1lllll_opy_ = {
                bstack11ll1l1_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ₆"): bstack11ll1l1_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧ₇"),
                bstack11ll1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ₈"): step[bstack11ll1l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ₉")],
                bstack11ll1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ₊"): step[bstack11ll1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ₋")],
                bstack11ll1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ₌"): step[bstack11ll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ₍")],
                bstack11ll1l1_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭₎"): step[bstack11ll1l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ₏")]
            }
            if bstack11ll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ₐ") in step:
                bstack1lllll1lllll_opy_[bstack11ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧₑ")] = step[bstack11ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨₒ")]
            elif bstack11ll1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩₓ") in step:
                bstack1lllll1lllll_opy_[bstack11ll1l1_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪₔ")] = step[bstack11ll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫₕ")]
            bstack1llllll111l1_opy_.append(bstack1lllll1lllll_opy_)
        cls.bstack11ll111ll1_opy_({
            bstack11ll1l1_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩₖ"): bstack11ll1l1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪₗ"),
            bstack11ll1l1_opy_ (u"ࠧ࡭ࡱࡪࡷࠬₘ"): bstack1llllll111l1_opy_
        })
    @classmethod
    @bstack111l1llll1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1ll11l1l11_opy_, stage=STAGE.bstack11l1lll1l1_opy_)
    def bstack1l1111ll1l_opy_(cls, screenshot):
        cls.bstack11ll111ll1_opy_({
            bstack11ll1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬₙ"): bstack11ll1l1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ₚ"),
            bstack11ll1l1_opy_ (u"ࠪࡰࡴ࡭ࡳࠨₛ"): [{
                bstack11ll1l1_opy_ (u"ࠫࡰ࡯࡮ࡥࠩₜ"): bstack11ll1l1_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧ₝"),
                bstack11ll1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ₞"): datetime.datetime.utcnow().isoformat() + bstack11ll1l1_opy_ (u"࡛ࠧࠩ₟"),
                bstack11ll1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ₠"): screenshot[bstack11ll1l1_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ₡")],
                bstack11ll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ₢"): screenshot[bstack11ll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ₣")]
            }]
        }, event_url=bstack11ll1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ₤"))
    @classmethod
    @bstack111l1llll1_opy_(class_method=True)
    def bstack1l1l1l1ll1_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11ll111ll1_opy_({
            bstack11ll1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ₥"): bstack11ll1l1_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ₦"),
            bstack11ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ₧"): {
                bstack11ll1l1_opy_ (u"ࠤࡸࡹ࡮ࡪࠢ₨"): cls.current_test_uuid(),
                bstack11ll1l1_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤ₩"): cls.bstack111llll1ll_opy_(driver)
            }
        })
    @classmethod
    def bstack111ll11lll_opy_(cls, event: str, bstack111l11llll_opy_: bstack1111ll1ll1_opy_):
        bstack111l1l1l11_opy_ = {
            bstack11ll1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ₪"): event,
            bstack111l11llll_opy_.bstack111l11ll1l_opy_(): bstack111l11llll_opy_.bstack111l111ll1_opy_(event)
        }
        cls.bstack11ll111ll1_opy_(bstack111l1l1l11_opy_)
        result = getattr(bstack111l11llll_opy_, bstack11ll1l1_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ₫"), None)
        if event == bstack11ll1l1_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ€"):
            threading.current_thread().bstackTestMeta = {bstack11ll1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ₭"): bstack11ll1l1_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ₮")}
        elif event == bstack11ll1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ₯"):
            threading.current_thread().bstackTestMeta = {bstack11ll1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ₰"): getattr(result, bstack11ll1l1_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ₱"), bstack11ll1l1_opy_ (u"ࠬ࠭₲"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ₳"), None) is None or os.environ[bstack11ll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ₴")] == bstack11ll1l1_opy_ (u"ࠣࡰࡸࡰࡱࠨ₵")) and (os.environ.get(bstack11ll1l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ₶"), None) is None or os.environ[bstack11ll1l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ₷")] == bstack11ll1l1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ₸")):
            return False
        return True
    @staticmethod
    def bstack1lllll11llll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1l11ll11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11ll1l1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ₹"): bstack11ll1l1_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ₺"),
            bstack11ll1l1_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪ₻"): bstack11ll1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭₼")
        }
        if os.environ.get(bstack11ll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭₽"), None):
            headers[bstack11ll1l1_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ₾")] = bstack11ll1l1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ₿").format(os.environ[bstack11ll1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠤ⃀")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11ll1l1_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬ⃁").format(bstack1lllll1l1l1l_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ⃂"), None)
    @staticmethod
    def bstack111llll1ll_opy_(driver):
        return {
            bstack11l111ll11l_opy_(): bstack11l111lll1l_opy_(driver)
        }
    @staticmethod
    def bstack1lllll1l1lll_opy_(exception_info, report):
        return [{bstack11ll1l1_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ⃃"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11111l1111_opy_(typename):
        if bstack11ll1l1_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧ⃄") in typename:
            return bstack11ll1l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦ⃅")
        return bstack11ll1l1_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧ⃆")