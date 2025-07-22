# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11ll1lll111_opy_, bstack11ll1l1lll1_opy_, bstack1llll111l_opy_, bstack111l1l1l1l_opy_, bstack11l11l111l1_opy_, bstack11l11ll1l11_opy_, bstack11l111l1111_opy_, bstack1ll1ll1l1_opy_, bstack1ll11lllll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111111l1l1l_opy_ import bstack111111l111l_opy_
import bstack_utils.bstack1ll11ll11l_opy_ as bstack1l1ll1l1ll_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack11llll1l11_opy_
import bstack_utils.accessibility as bstack1l1ll11l1l_opy_
from bstack_utils.bstack111lll1ll_opy_ import bstack111lll1ll_opy_
from bstack_utils.bstack111ll1ll1l_opy_ import bstack1111ll1lll_opy_
bstack1lllll1ll1ll_opy_ = bstack111l111_opy_ (u"ࠫ࡭ࡺࡴࡱࡵ࠽࠳࠴ࡩ࡯࡭࡮ࡨࡧࡹࡵࡲ࠮ࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫ‐")
logger = logging.getLogger(__name__)
class bstack1l1ll1l11_opy_:
    bstack111111l1l1l_opy_ = None
    bs_config = None
    bstack11l1l1l11l_opy_ = None
    @classmethod
    @bstack111l1l1l1l_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11l1l1llll1_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def launch(cls, bs_config, bstack11l1l1l11l_opy_):
        cls.bs_config = bs_config
        cls.bstack11l1l1l11l_opy_ = bstack11l1l1l11l_opy_
        try:
            cls.bstack1lllll11llll_opy_()
            bstack11ll1l11111_opy_ = bstack11ll1lll111_opy_(bs_config)
            bstack11ll1l11l1l_opy_ = bstack11ll1l1lll1_opy_(bs_config)
            data = bstack1l1ll1l1ll_opy_.bstack1llllll11111_opy_(bs_config, bstack11l1l1l11l_opy_)
            config = {
                bstack111l111_opy_ (u"ࠬࡧࡵࡵࡪࠪ‑"): (bstack11ll1l11111_opy_, bstack11ll1l11l1l_opy_),
                bstack111l111_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ‒"): cls.default_headers()
            }
            response = bstack1llll111l_opy_(bstack111l111_opy_ (u"ࠧࡑࡑࡖࡘࠬ–"), cls.request_url(bstack111l111_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠲࠰ࡤࡸ࡭ࡱࡪࡳࠨ—")), data, config)
            if response.status_code != 200:
                bstack11l1111l11_opy_ = response.json()
                if bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ―")] == False:
                    cls.bstack1lllll1lllll_opy_(bstack11l1111l11_opy_)
                    return
                cls.bstack1lllll1ll11l_opy_(bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ‖")])
                cls.bstack1lllll11l1l1_opy_(bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ‗")])
                return None
            bstack1lllll1l1111_opy_ = cls.bstack1lllll1l11ll_opy_(response)
            return bstack1lllll1l1111_opy_, response.json()
        except Exception as error:
            logger.error(bstack111l111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡥࡹ࡮ࡲࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡼࡿࠥ‘").format(str(error)))
            return None
    @classmethod
    @bstack111l1l1l1l_opy_(class_method=True)
    def stop(cls, bstack1lllll1llll1_opy_=None):
        if not bstack11llll1l11_opy_.on() and not bstack1l1ll11l1l_opy_.on():
            return
        if os.environ.get(bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ’")) == bstack111l111_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ‚") or os.environ.get(bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭‛")) == bstack111l111_opy_ (u"ࠤࡱࡹࡱࡲࠢ“"):
            logger.error(bstack111l111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡴࡶࠠࡣࡷ࡬ࡰࡩࠦࡲࡦࡳࡸࡩࡸࡺࠠࡵࡱࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭”"))
            return {
                bstack111l111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ„"): bstack111l111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ‟"),
                bstack111l111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ†"): bstack111l111_opy_ (u"ࠧࡕࡱ࡮ࡩࡳ࠵ࡢࡶ࡫࡯ࡨࡎࡊࠠࡪࡵࠣࡹࡳࡪࡥࡧ࡫ࡱࡩࡩ࠲ࠠࡣࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡ࡯࡬࡫࡭ࡺࠠࡩࡣࡹࡩࠥ࡬ࡡࡪ࡮ࡨࡨࠬ‡")
            }
        try:
            cls.bstack111111l1l1l_opy_.shutdown()
            data = {
                bstack111l111_opy_ (u"ࠨࡨ࡬ࡲ࡮ࡹࡨࡦࡦࡢࡥࡹ࠭•"): bstack1ll1ll1l1_opy_()
            }
            if not bstack1lllll1llll1_opy_ is None:
                data[bstack111l111_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡲ࡫ࡴࡢࡦࡤࡸࡦ࠭‣")] = [{
                    bstack111l111_opy_ (u"ࠪࡶࡪࡧࡳࡰࡰࠪ․"): bstack111l111_opy_ (u"ࠫࡺࡹࡥࡳࡡ࡮࡭ࡱࡲࡥࡥࠩ‥"),
                    bstack111l111_opy_ (u"ࠬࡹࡩࡨࡰࡤࡰࠬ…"): bstack1lllll1llll1_opy_
                }]
            config = {
                bstack111l111_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ‧"): cls.default_headers()
            }
            bstack11ll11l1l11_opy_ = bstack111l111_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿ࠲ࡷࡹࡵࡰࠨ ").format(os.environ[bstack111l111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉࠨ ")])
            bstack1lllll1lll11_opy_ = cls.request_url(bstack11ll11l1l11_opy_)
            response = bstack1llll111l_opy_(bstack111l111_opy_ (u"ࠩࡓ࡙࡙࠭‪"), bstack1lllll1lll11_opy_, data, config)
            if not response.ok:
                raise Exception(bstack111l111_opy_ (u"ࠥࡗࡹࡵࡰࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡱࡳࡹࠦ࡯࡬ࠤ‫"))
        except Exception as error:
            logger.error(bstack111l111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࡀࠠࠣ‬") + str(error))
            return {
                bstack111l111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ‭"): bstack111l111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ‮"),
                bstack111l111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ "): str(error)
            }
    @classmethod
    @bstack111l1l1l1l_opy_(class_method=True)
    def bstack1lllll1l11ll_opy_(cls, response):
        bstack11l1111l11_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1lllll1l1111_opy_ = {}
        if bstack11l1111l11_opy_.get(bstack111l111_opy_ (u"ࠨ࡬ࡺࡸࠬ‰")) is None:
            os.environ[bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭‱")] = bstack111l111_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ′")
        else:
            os.environ[bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ″")] = bstack11l1111l11_opy_.get(bstack111l111_opy_ (u"ࠬࡰࡷࡵࠩ‴"), bstack111l111_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ‵"))
        os.environ[bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ‶")] = bstack11l1111l11_opy_.get(bstack111l111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ‷"), bstack111l111_opy_ (u"ࠩࡱࡹࡱࡲࠧ‸"))
        logger.info(bstack111l111_opy_ (u"ࠪࡘࡪࡹࡴࡩࡷࡥࠤࡸࡺࡡࡳࡶࡨࡨࠥࡽࡩࡵࡪࠣ࡭ࡩࡀࠠࠨ‹") + os.getenv(bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ›")));
        if bstack11llll1l11_opy_.bstack1lllll11l1ll_opy_(cls.bs_config, cls.bstack11l1l1l11l_opy_.get(bstack111l111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭※"), bstack111l111_opy_ (u"࠭ࠧ‼"))) is True:
            bstack1111111l11l_opy_, build_hashed_id, bstack1lllll11lll1_opy_ = cls.bstack1llllll1111l_opy_(bstack11l1111l11_opy_)
            if bstack1111111l11l_opy_ != None and build_hashed_id != None:
                bstack1lllll1l1111_opy_[bstack111l111_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ‽")] = {
                    bstack111l111_opy_ (u"ࠨ࡬ࡺࡸࡤࡺ࡯࡬ࡧࡱࠫ‾"): bstack1111111l11l_opy_,
                    bstack111l111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ‿"): build_hashed_id,
                    bstack111l111_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧ⁀"): bstack1lllll11lll1_opy_
                }
            else:
                bstack1lllll1l1111_opy_[bstack111l111_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⁁")] = {}
        else:
            bstack1lllll1l1111_opy_[bstack111l111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⁂")] = {}
        bstack1lllll1l11l1_opy_, build_hashed_id = cls.bstack1lllll1ll1l1_opy_(bstack11l1111l11_opy_)
        if bstack1lllll1l11l1_opy_ != None and build_hashed_id != None:
            bstack1lllll1l1111_opy_[bstack111l111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⁃")] = {
                bstack111l111_opy_ (u"ࠧࡢࡷࡷ࡬ࡤࡺ࡯࡬ࡧࡱࠫ⁄"): bstack1lllll1l11l1_opy_,
                bstack111l111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⁅"): build_hashed_id,
            }
        else:
            bstack1lllll1l1111_opy_[bstack111l111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⁆")] = {}
        if bstack1lllll1l1111_opy_[bstack111l111_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⁇")].get(bstack111l111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⁈")) != None or bstack1lllll1l1111_opy_[bstack111l111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⁉")].get(bstack111l111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⁊")) != None:
            cls.bstack1lllll1l1lll_opy_(bstack11l1111l11_opy_.get(bstack111l111_opy_ (u"ࠧ࡫ࡹࡷࠫ⁋")), bstack11l1111l11_opy_.get(bstack111l111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⁌")))
        return bstack1lllll1l1111_opy_
    @classmethod
    def bstack1llllll1111l_opy_(cls, bstack11l1111l11_opy_):
        if bstack11l1111l11_opy_.get(bstack111l111_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⁍")) == None:
            cls.bstack1lllll1ll11l_opy_()
            return [None, None, None]
        if bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⁎")][bstack111l111_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ⁏")] != True:
            cls.bstack1lllll1ll11l_opy_(bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⁐")])
            return [None, None, None]
        logger.debug(bstack111l111_opy_ (u"࠭ࡔࡦࡵࡷࠤࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ⁑"))
        os.environ[bstack111l111_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡇࡔࡓࡐࡍࡇࡗࡉࡉ࠭⁒")] = bstack111l111_opy_ (u"ࠨࡶࡵࡹࡪ࠭⁓")
        if bstack11l1111l11_opy_.get(bstack111l111_opy_ (u"ࠩ࡭ࡻࡹ࠭⁔")):
            os.environ[bstack111l111_opy_ (u"ࠪࡇࡗࡋࡄࡆࡐࡗࡍࡆࡒࡓࡠࡈࡒࡖࡤࡉࡒࡂࡕࡋࡣࡗࡋࡐࡐࡔࡗࡍࡓࡍࠧ⁕")] = json.dumps({
                bstack111l111_opy_ (u"ࠫࡺࡹࡥࡳࡰࡤࡱࡪ࠭⁖"): bstack11ll1lll111_opy_(cls.bs_config),
                bstack111l111_opy_ (u"ࠬࡶࡡࡴࡵࡺࡳࡷࡪࠧ⁗"): bstack11ll1l1lll1_opy_(cls.bs_config)
            })
        if bstack11l1111l11_opy_.get(bstack111l111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ⁘")):
            os.environ[bstack111l111_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭⁙")] = bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⁚")]
        if bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⁛")].get(bstack111l111_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ⁜"), {}).get(bstack111l111_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ⁝")):
            os.environ[bstack111l111_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭⁞")] = str(bstack11l1111l11_opy_[bstack111l111_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ ")][bstack111l111_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ⁠")][bstack111l111_opy_ (u"ࠨࡣ࡯ࡰࡴࡽ࡟ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ⁡")])
        else:
            os.environ[bstack111l111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ⁢")] = bstack111l111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ⁣")
        return [bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠫ࡯ࡽࡴࠨ⁤")], bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ⁥")], os.environ[bstack111l111_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧ⁦")]]
    @classmethod
    def bstack1lllll1ll1l1_opy_(cls, bstack11l1111l11_opy_):
        if bstack11l1111l11_opy_.get(bstack111l111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⁧")) == None:
            cls.bstack1lllll11l1l1_opy_()
            return [None, None]
        if bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⁨")][bstack111l111_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ⁩")] != True:
            cls.bstack1lllll11l1l1_opy_(bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⁪")])
            return [None, None]
        if bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⁫")].get(bstack111l111_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭⁬")):
            logger.debug(bstack111l111_opy_ (u"࠭ࡔࡦࡵࡷࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪ⁭"))
            parsed = json.loads(os.getenv(bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ⁮"), bstack111l111_opy_ (u"ࠨࡽࢀࠫ⁯")))
            capabilities = bstack1l1ll1l1ll_opy_.bstack1lllll11ll1l_opy_(bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⁰")][bstack111l111_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫⁱ")][bstack111l111_opy_ (u"ࠫࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ⁲")], bstack111l111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⁳"), bstack111l111_opy_ (u"࠭ࡶࡢ࡮ࡸࡩࠬ⁴"))
            bstack1lllll1l11l1_opy_ = capabilities[bstack111l111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬ⁵")]
            os.environ[bstack111l111_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭⁶")] = bstack1lllll1l11l1_opy_
            if bstack111l111_opy_ (u"ࠤࡤࡹࡹࡵ࡭ࡢࡶࡨࠦ⁷") in bstack11l1111l11_opy_ and bstack11l1111l11_opy_.get(bstack111l111_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤ⁸")) is None:
                parsed[bstack111l111_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ⁹")] = capabilities[bstack111l111_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⁺")]
            os.environ[bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ⁻")] = json.dumps(parsed)
            scripts = bstack1l1ll1l1ll_opy_.bstack1lllll11ll1l_opy_(bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⁼")][bstack111l111_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⁽")][bstack111l111_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪ⁾")], bstack111l111_opy_ (u"ࠪࡲࡦࡳࡥࠨⁿ"), bstack111l111_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࠬ₀"))
            bstack111lll1ll_opy_.bstack11lll111l_opy_(scripts)
            commands = bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ₁")][bstack111l111_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ₂")][bstack111l111_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࡖࡲ࡛ࡷࡧࡰࠨ₃")].get(bstack111l111_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ₄"))
            bstack111lll1ll_opy_.bstack11ll11lll11_opy_(commands)
            bstack11ll1ll1ll1_opy_ = capabilities.get(bstack111l111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ₅"))
            bstack111lll1ll_opy_.bstack11ll11l1ll1_opy_(bstack11ll1ll1ll1_opy_)
            bstack111lll1ll_opy_.store()
        return [bstack1lllll1l11l1_opy_, bstack11l1111l11_opy_[bstack111l111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬ₆")]]
    @classmethod
    def bstack1lllll1ll11l_opy_(cls, response=None):
        os.environ[bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ₇")] = bstack111l111_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ₈")
        os.environ[bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ₉")] = bstack111l111_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ₊")
        os.environ[bstack111l111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧ₋")] = bstack111l111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ₌")
        os.environ[bstack111l111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ₍")] = bstack111l111_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ₎")
        os.environ[bstack111l111_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭₏")] = bstack111l111_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦₐ")
        cls.bstack1lllll1lllll_opy_(response, bstack111l111_opy_ (u"ࠢࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠢₑ"))
        return [None, None, None]
    @classmethod
    def bstack1lllll11l1l1_opy_(cls, response=None):
        os.environ[bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ₒ")] = bstack111l111_opy_ (u"ࠩࡱࡹࡱࡲࠧₓ")
        os.environ[bstack111l111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨₔ")] = bstack111l111_opy_ (u"ࠫࡳࡻ࡬࡭ࠩₕ")
        os.environ[bstack111l111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩₖ")] = bstack111l111_opy_ (u"࠭࡮ࡶ࡮࡯ࠫₗ")
        cls.bstack1lllll1lllll_opy_(response, bstack111l111_opy_ (u"ࠢࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠢₘ"))
        return [None, None, None]
    @classmethod
    def bstack1lllll1l1lll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬₙ")] = jwt
        os.environ[bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧₚ")] = build_hashed_id
    @classmethod
    def bstack1lllll1lllll_opy_(cls, response=None, product=bstack111l111_opy_ (u"ࠥࠦₛ")):
        if response == None or response.get(bstack111l111_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫₜ")) == None:
            logger.error(product + bstack111l111_opy_ (u"ࠧࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡧࡣ࡬ࡰࡪࡪࠢ₝"))
            return
        for error in response[bstack111l111_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭₞")]:
            bstack11l1111ll11_opy_ = error[bstack111l111_opy_ (u"ࠧ࡬ࡧࡼࠫ₟")]
            error_message = error[bstack111l111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ₠")]
            if error_message:
                if bstack11l1111ll11_opy_ == bstack111l111_opy_ (u"ࠤࡈࡖࡗࡕࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡆࡈࡒࡎࡋࡄࠣ₡"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack111l111_opy_ (u"ࠥࡈࡦࡺࡡࠡࡷࡳࡰࡴࡧࡤࠡࡶࡲࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࠦ₢") + product + bstack111l111_opy_ (u"ࠦࠥ࡬ࡡࡪ࡮ࡨࡨࠥࡪࡵࡦࠢࡷࡳࠥࡹ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠤ₣"))
    @classmethod
    def bstack1lllll11llll_opy_(cls):
        if cls.bstack111111l1l1l_opy_ is not None:
            return
        cls.bstack111111l1l1l_opy_ = bstack111111l111l_opy_(cls.bstack1lllll11l11l_opy_)
        cls.bstack111111l1l1l_opy_.start()
    @classmethod
    def bstack111l111l11_opy_(cls):
        if cls.bstack111111l1l1l_opy_ is None:
            return
        cls.bstack111111l1l1l_opy_.shutdown()
    @classmethod
    @bstack111l1l1l1l_opy_(class_method=True)
    def bstack1lllll11l11l_opy_(cls, bstack111l11111l_opy_, event_url=bstack111l111_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ₤")):
        config = {
            bstack111l111_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ₥"): cls.default_headers()
        }
        logger.debug(bstack111l111_opy_ (u"ࠢࡱࡱࡶࡸࡤࡪࡡࡵࡣ࠽ࠤࡘ࡫࡮ࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡸࡴࠦࡴࡦࡵࡷ࡬ࡺࡨࠠࡧࡱࡵࠤࡪࡼࡥ࡯ࡶࡶࠤࢀࢃࠢ₦").format(bstack111l111_opy_ (u"ࠨ࠮ࠣࠫ₧").join([event[bstack111l111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭₨")] for event in bstack111l11111l_opy_])))
        response = bstack1llll111l_opy_(bstack111l111_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ₩"), cls.request_url(event_url), bstack111l11111l_opy_, config)
        bstack11ll1llll11_opy_ = response.json()
    @classmethod
    def bstack1ll1ll1ll1_opy_(cls, bstack111l11111l_opy_, event_url=bstack111l111_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ₪")):
        logger.debug(bstack111l111_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡸࡹ࡫࡭ࡱࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡤࡨࡩࠦࡤࡢࡶࡤࠤࡹࡵࠠࡣࡣࡷࡧ࡭ࠦࡷࡪࡶ࡫ࠤࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥ࠻ࠢࡾࢁࠧ₫").format(bstack111l11111l_opy_[bstack111l111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ€")]))
        if not bstack1l1ll1l1ll_opy_.bstack1lllll1l1l1l_opy_(bstack111l11111l_opy_[bstack111l111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ₭")]):
            logger.debug(bstack111l111_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡔ࡯ࡵࠢࡤࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨ₮").format(bstack111l11111l_opy_[bstack111l111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭₯")]))
            return
        bstack1ll11llll1_opy_ = bstack1l1ll1l1ll_opy_.bstack1lllll1l1l11_opy_(bstack111l11111l_opy_[bstack111l111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ₰")], bstack111l11111l_opy_.get(bstack111l111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭₱")))
        if bstack1ll11llll1_opy_ != None:
            if bstack111l11111l_opy_.get(bstack111l111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧ₲")) != None:
                bstack111l11111l_opy_[bstack111l111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ₳")][bstack111l111_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ₴")] = bstack1ll11llll1_opy_
            else:
                bstack111l11111l_opy_[bstack111l111_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭₵")] = bstack1ll11llll1_opy_
        if event_url == bstack111l111_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨ₶"):
            cls.bstack1lllll11llll_opy_()
            logger.debug(bstack111l111_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡂࡦࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨ₷").format(bstack111l11111l_opy_[bstack111l111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ₸")]))
            cls.bstack111111l1l1l_opy_.add(bstack111l11111l_opy_)
        elif event_url == bstack111l111_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ₹"):
            cls.bstack1lllll11l11l_opy_([bstack111l11111l_opy_], event_url)
    @classmethod
    @bstack111l1l1l1l_opy_(class_method=True)
    def bstack1l1111ll1l_opy_(cls, logs):
        for log in logs:
            bstack1lllll1l111l_opy_ = {
                bstack111l111_opy_ (u"࠭࡫ࡪࡰࡧࠫ₺"): bstack111l111_opy_ (u"ࠧࡕࡇࡖࡘࡤࡒࡏࡈࠩ₻"),
                bstack111l111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ₼"): log[bstack111l111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ₽")],
                bstack111l111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭₾"): log[bstack111l111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ₿")],
                bstack111l111_opy_ (u"ࠬ࡮ࡴࡵࡲࡢࡶࡪࡹࡰࡰࡰࡶࡩࠬ⃀"): {},
                bstack111l111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⃁"): log[bstack111l111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ⃂")],
            }
            if bstack111l111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⃃") in log:
                bstack1lllll1l111l_opy_[bstack111l111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⃄")] = log[bstack111l111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⃅")]
            elif bstack111l111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⃆") in log:
                bstack1lllll1l111l_opy_[bstack111l111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⃇")] = log[bstack111l111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⃈")]
            cls.bstack1ll1ll1ll1_opy_({
                bstack111l111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⃉"): bstack111l111_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⃊"),
                bstack111l111_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ⃋"): [bstack1lllll1l111l_opy_]
            })
    @classmethod
    @bstack111l1l1l1l_opy_(class_method=True)
    def bstack1lllll11l111_opy_(cls, steps):
        bstack1lllll11ll11_opy_ = []
        for step in steps:
            bstack1lllll1l1ll1_opy_ = {
                bstack111l111_opy_ (u"ࠪ࡯࡮ࡴࡤࠨ⃌"): bstack111l111_opy_ (u"࡙ࠫࡋࡓࡕࡡࡖࡘࡊࡖࠧ⃍"),
                bstack111l111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ⃎"): step[bstack111l111_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ⃏")],
                bstack111l111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ⃐"): step[bstack111l111_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⃑")],
                bstack111l111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧ⃒ࠪ"): step[bstack111l111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨ⃓ࠫ")],
                bstack111l111_opy_ (u"ࠫࡩࡻࡲࡢࡶ࡬ࡳࡳ࠭⃔"): step[bstack111l111_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ⃕")]
            }
            if bstack111l111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⃖") in step:
                bstack1lllll1l1ll1_opy_[bstack111l111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⃗")] = step[bstack111l111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⃘")]
            elif bstack111l111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥ⃙ࠩ") in step:
                bstack1lllll1l1ll1_opy_[bstack111l111_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦ⃚ࠪ")] = step[bstack111l111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⃛")]
            bstack1lllll11ll11_opy_.append(bstack1lllll1l1ll1_opy_)
        cls.bstack1ll1ll1ll1_opy_({
            bstack111l111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ⃜"): bstack111l111_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ⃝"),
            bstack111l111_opy_ (u"ࠧ࡭ࡱࡪࡷࠬ⃞"): bstack1lllll11ll11_opy_
        })
    @classmethod
    @bstack111l1l1l1l_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll1111l_opy_, stage=STAGE.bstack11l1llll1_opy_)
    def bstack1ll1l1lll_opy_(cls, screenshot):
        cls.bstack1ll1ll1ll1_opy_({
            bstack111l111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⃟"): bstack111l111_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭⃠"),
            bstack111l111_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ⃡"): [{
                bstack111l111_opy_ (u"ࠫࡰ࡯࡮ࡥࠩ⃢"): bstack111l111_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࠧ⃣"),
                bstack111l111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ⃤"): datetime.datetime.utcnow().isoformat() + bstack111l111_opy_ (u"⃥࡛ࠧࠩ"),
                bstack111l111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦ⃦ࠩ"): screenshot[bstack111l111_opy_ (u"ࠩ࡬ࡱࡦ࡭ࡥࠨ⃧")],
                bstack111l111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦ⃨ࠪ"): screenshot[bstack111l111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⃩")]
            }]
        }, event_url=bstack111l111_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵ⃪ࠪ"))
    @classmethod
    @bstack111l1l1l1l_opy_(class_method=True)
    def bstack1l11l1llll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1ll1ll1ll1_opy_({
            bstack111l111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ⃫ࠪ"): bstack111l111_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧ⃬ࠫ"),
            bstack111l111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰ⃭ࠪ"): {
                bstack111l111_opy_ (u"ࠤࡸࡹ࡮ࡪ⃮ࠢ"): cls.current_test_uuid(),
                bstack111l111_opy_ (u"ࠥ࡭ࡳࡺࡥࡨࡴࡤࡸ࡮ࡵ࡮ࡴࠤ⃯"): cls.bstack111lll1l11_opy_(driver)
            }
        })
    @classmethod
    def bstack111ll1l1ll_opy_(cls, event: str, bstack111l11111l_opy_: bstack1111ll1lll_opy_):
        bstack1111lllll1_opy_ = {
            bstack111l111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⃰"): event,
            bstack111l11111l_opy_.bstack111l111111_opy_(): bstack111l11111l_opy_.bstack111l1l1ll1_opy_(event)
        }
        cls.bstack1ll1ll1ll1_opy_(bstack1111lllll1_opy_)
        result = getattr(bstack111l11111l_opy_, bstack111l111_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ⃱"), None)
        if event == bstack111l111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⃲"):
            threading.current_thread().bstackTestMeta = {bstack111l111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⃳"): bstack111l111_opy_ (u"ࠨࡲࡨࡲࡩ࡯࡮ࡨࠩ⃴")}
        elif event == bstack111l111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⃵"):
            threading.current_thread().bstackTestMeta = {bstack111l111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ⃶"): getattr(result, bstack111l111_opy_ (u"ࠫࡷ࡫ࡳࡶ࡮ࡷࠫ⃷"), bstack111l111_opy_ (u"ࠬ࠭⃸"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ⃹"), None) is None or os.environ[bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ⃺")] == bstack111l111_opy_ (u"ࠣࡰࡸࡰࡱࠨ⃻")) and (os.environ.get(bstack111l111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ⃼"), None) is None or os.environ[bstack111l111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ⃽")] == bstack111l111_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⃾")):
            return False
        return True
    @staticmethod
    def bstack1lllll1lll1l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1ll1l11_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack111l111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ⃿"): bstack111l111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ℀"),
            bstack111l111_opy_ (u"࡙ࠧ࠯ࡅࡗ࡙ࡇࡃࡌ࠯ࡗࡉࡘ࡚ࡏࡑࡕࠪ℁"): bstack111l111_opy_ (u"ࠨࡶࡵࡹࡪ࠭ℂ")
        }
        if os.environ.get(bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭℃"), None):
            headers[bstack111l111_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪ℄")] = bstack111l111_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࢀࢃࠧ℅").format(os.environ[bstack111l111_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠤ℆")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack111l111_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬℇ").format(bstack1lllll1ll1ll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack111l111_opy_ (u"ࠧࡤࡷࡵࡶࡪࡴࡴࡠࡶࡨࡷࡹࡥࡵࡶ࡫ࡧࠫ℈"), None)
    @staticmethod
    def bstack111lll1l11_opy_(driver):
        return {
            bstack11l11l111l1_opy_(): bstack11l11ll1l11_opy_(driver)
        }
    @staticmethod
    def bstack1lllll1ll111_opy_(exception_info, report):
        return [{bstack111l111_opy_ (u"ࠨࡤࡤࡧࡰࡺࡲࡢࡥࡨࠫ℉"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111111llll_opy_(typename):
        if bstack111l111_opy_ (u"ࠤࡄࡷࡸ࡫ࡲࡵ࡫ࡲࡲࠧℊ") in typename:
            return bstack111l111_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࡋࡲࡳࡱࡵࠦℋ")
        return bstack111l111_opy_ (u"࡚ࠦࡴࡨࡢࡰࡧࡰࡪࡪࡅࡳࡴࡲࡶࠧℌ")