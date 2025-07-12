# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l11l1llll_opy_, bstack11l11ll111l_opy_, bstack1lllll1111_opy_, bstack111l11l1l1_opy_, bstack111ll11l111_opy_, bstack111l1111l1l_opy_, bstack1111llll11l_opy_, bstack1lllllllll_opy_, bstack11ll1lll_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack111111ll1ll_opy_ import bstack111111lll1l_opy_
import bstack_utils.bstack11l111lll1_opy_ as bstack1ll1lll11_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1l1ll111ll_opy_
import bstack_utils.accessibility as bstack11llll1l11_opy_
from bstack_utils.bstack11llll1111_opy_ import bstack11llll1111_opy_
from bstack_utils.bstack111ll1ll1l_opy_ import bstack111l11lll1_opy_
bstack1lllll11lll1_opy_ = bstack11l1111_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡥࡲࡰࡱ࡫ࡣࡵࡱࡵ࠱ࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡳࠧ‌")
logger = logging.getLogger(__name__)
class bstack111lll111_opy_:
    bstack111111ll1ll_opy_ = None
    bs_config = None
    bstack1ll111ll1_opy_ = None
    @classmethod
    @bstack111l11l1l1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11l11111ll1_opy_, stage=STAGE.bstack1111llll1_opy_)
    def launch(cls, bs_config, bstack1ll111ll1_opy_):
        cls.bs_config = bs_config
        cls.bstack1ll111ll1_opy_ = bstack1ll111ll1_opy_
        try:
            cls.bstack1lllll11ll1l_opy_()
            bstack11l11ll1l11_opy_ = bstack11l11l1llll_opy_(bs_config)
            bstack11l11ll11ll_opy_ = bstack11l11ll111l_opy_(bs_config)
            data = bstack1ll1lll11_opy_.bstack1lllll1ll1l1_opy_(bs_config, bstack1ll111ll1_opy_)
            config = {
                bstack11l1111_opy_ (u"ࠨࡣࡸࡸ࡭࠭‍"): (bstack11l11ll1l11_opy_, bstack11l11ll11ll_opy_),
                bstack11l1111_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ‎"): cls.default_headers()
            }
            response = bstack1lllll1111_opy_(bstack11l1111_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ‏"), cls.request_url(bstack11l1111_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠵࠳ࡧࡻࡩ࡭ࡦࡶࠫ‐")), data, config)
            if response.status_code != 200:
                bstack11l11l11_opy_ = response.json()
                if bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭‑")] == False:
                    cls.bstack1lllll11llll_opy_(bstack11l11l11_opy_)
                    return
                cls.bstack1lllll1l1111_opy_(bstack11l11l11_opy_[bstack11l1111_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭‒")])
                cls.bstack1lllll11ll11_opy_(bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ–")])
                return None
            bstack1lllll1l111l_opy_ = cls.bstack1lllll11l1l1_opy_(response)
            return bstack1lllll1l111l_opy_, response.json()
        except Exception as error:
            logger.error(bstack11l1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡨࡵࡪ࡮ࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࡿࢂࠨ—").format(str(error)))
            return None
    @classmethod
    @bstack111l11l1l1_opy_(class_method=True)
    def stop(cls, bstack1lllll1l1l11_opy_=None):
        if not bstack1l1ll111ll_opy_.on() and not bstack11llll1l11_opy_.on():
            return
        if os.environ.get(bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭―")) == bstack11l1111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ‖") or os.environ.get(bstack11l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ‗")) == bstack11l1111_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ‘"):
            logger.error(bstack11l1111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩ’"))
            return {
                bstack11l1111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ‚"): bstack11l1111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ‛"),
                bstack11l1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ“"): bstack11l1111_opy_ (u"ࠪࡘࡴࡱࡥ࡯࠱ࡥࡹ࡮ࡲࡤࡊࡆࠣ࡭ࡸࠦࡵ࡯ࡦࡨࡪ࡮ࡴࡥࡥ࠮ࠣࡦࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤࡲ࡯ࡧࡩࡶࠣ࡬ࡦࡼࡥࠡࡨࡤ࡭ࡱ࡫ࡤࠨ”")
            }
        try:
            cls.bstack111111ll1ll_opy_.shutdown()
            data = {
                bstack11l1111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩ„"): bstack1lllllllll_opy_()
            }
            if not bstack1lllll1l1l11_opy_ is None:
                data[bstack11l1111_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟࡮ࡧࡷࡥࡩࡧࡴࡢࠩ‟")] = [{
                    bstack11l1111_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭†"): bstack11l1111_opy_ (u"ࠧࡶࡵࡨࡶࡤࡱࡩ࡭࡮ࡨࡨࠬ‡"),
                    bstack11l1111_opy_ (u"ࠨࡵ࡬࡫ࡳࡧ࡬ࠨ•"): bstack1lllll1l1l11_opy_
                }]
            config = {
                bstack11l1111_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ‣"): cls.default_headers()
            }
            bstack11ll111ll11_opy_ = bstack11l1111_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡺ࡯࡬ࡥࡵ࠲ࡿࢂ࠵ࡳࡵࡱࡳࠫ․").format(os.environ[bstack11l1111_opy_ (u"ࠦࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠤ‥")])
            bstack1lllll1lll11_opy_ = cls.request_url(bstack11ll111ll11_opy_)
            response = bstack1lllll1111_opy_(bstack11l1111_opy_ (u"ࠬࡖࡕࡕࠩ…"), bstack1lllll1lll11_opy_, data, config)
            if not response.ok:
                raise Exception(bstack11l1111_opy_ (u"ࠨࡓࡵࡱࡳࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡴ࡯ࡵࠢࡲ࡯ࠧ‧"))
        except Exception as error:
            logger.error(bstack11l1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻࠼ࠣࠦ ") + str(error))
            return {
                bstack11l1111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ "): bstack11l1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨ‪"),
                bstack11l1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ‫"): str(error)
            }
    @classmethod
    @bstack111l11l1l1_opy_(class_method=True)
    def bstack1lllll11l1l1_opy_(cls, response):
        bstack11l11l11_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1lllll1l111l_opy_ = {}
        if bstack11l11l11_opy_.get(bstack11l1111_opy_ (u"ࠫ࡯ࡽࡴࠨ‬")) is None:
            os.environ[bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ‭")] = bstack11l1111_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ‮")
        else:
            os.environ[bstack11l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ ")] = bstack11l11l11_opy_.get(bstack11l1111_opy_ (u"ࠨ࡬ࡺࡸࠬ‰"), bstack11l1111_opy_ (u"ࠩࡱࡹࡱࡲࠧ‱"))
        os.environ[bstack11l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ′")] = bstack11l11l11_opy_.get(bstack11l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭″"), bstack11l1111_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ‴"))
        logger.info(bstack11l1111_opy_ (u"࠭ࡔࡦࡵࡷ࡬ࡺࡨࠠࡴࡶࡤࡶࡹ࡫ࡤࠡࡹ࡬ࡸ࡭ࠦࡩࡥ࠼ࠣࠫ‵") + os.getenv(bstack11l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ‶")));
        if bstack1l1ll111ll_opy_.bstack1lllll1lll1l_opy_(cls.bs_config, cls.bstack1ll111ll1_opy_.get(bstack11l1111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ‷"), bstack11l1111_opy_ (u"ࠩࠪ‸"))) is True:
            bstack1111111lll1_opy_, build_hashed_id, bstack1llllll111l1_opy_ = cls.bstack1lllll1lllll_opy_(bstack11l11l11_opy_)
            if bstack1111111lll1_opy_ != None and build_hashed_id != None:
                bstack1lllll1l111l_opy_[bstack11l1111_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ‹")] = {
                    bstack11l1111_opy_ (u"ࠫ࡯ࡽࡴࡠࡶࡲ࡯ࡪࡴࠧ›"): bstack1111111lll1_opy_,
                    bstack11l1111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧ※"): build_hashed_id,
                    bstack11l1111_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ‼"): bstack1llllll111l1_opy_
                }
            else:
                bstack1lllll1l111l_opy_[bstack11l1111_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ‽")] = {}
        else:
            bstack1lllll1l111l_opy_[bstack11l1111_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ‾")] = {}
        bstack1llllll11111_opy_, build_hashed_id = cls.bstack1lllll1ll111_opy_(bstack11l11l11_opy_)
        if bstack1llllll11111_opy_ != None and build_hashed_id != None:
            bstack1lllll1l111l_opy_[bstack11l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ‿")] = {
                bstack11l1111_opy_ (u"ࠪࡥࡺࡺࡨࡠࡶࡲ࡯ࡪࡴࠧ⁀"): bstack1llllll11111_opy_,
                bstack11l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⁁"): build_hashed_id,
            }
        else:
            bstack1lllll1l111l_opy_[bstack11l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⁂")] = {}
        if bstack1lllll1l111l_opy_[bstack11l1111_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⁃")].get(bstack11l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩ⁄")) != None or bstack1lllll1l111l_opy_[bstack11l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⁅")].get(bstack11l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⁆")) != None:
            cls.bstack1llllll1111l_opy_(bstack11l11l11_opy_.get(bstack11l1111_opy_ (u"ࠪ࡮ࡼࡺࠧ⁇")), bstack11l11l11_opy_.get(bstack11l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⁈")))
        return bstack1lllll1l111l_opy_
    @classmethod
    def bstack1lllll1lllll_opy_(cls, bstack11l11l11_opy_):
        if bstack11l11l11_opy_.get(bstack11l1111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⁉")) == None:
            cls.bstack1lllll1l1111_opy_()
            return [None, None, None]
        if bstack11l11l11_opy_[bstack11l1111_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⁊")][bstack11l1111_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ⁋")] != True:
            cls.bstack1lllll1l1111_opy_(bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⁌")])
            return [None, None, None]
        logger.debug(bstack11l1111_opy_ (u"ࠩࡗࡩࡸࡺࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭⁍"))
        os.environ[bstack11l1111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩ⁎")] = bstack11l1111_opy_ (u"ࠫࡹࡸࡵࡦࠩ⁏")
        if bstack11l11l11_opy_.get(bstack11l1111_opy_ (u"ࠬࡰࡷࡵࠩ⁐")):
            os.environ[bstack11l1111_opy_ (u"࠭ࡃࡓࡇࡇࡉࡓ࡚ࡉࡂࡎࡖࡣࡋࡕࡒࡠࡅࡕࡅࡘࡎ࡟ࡓࡇࡓࡓࡗ࡚ࡉࡏࡉࠪ⁑")] = json.dumps({
                bstack11l1111_opy_ (u"ࠧࡶࡵࡨࡶࡳࡧ࡭ࡦࠩ⁒"): bstack11l11l1llll_opy_(cls.bs_config),
                bstack11l1111_opy_ (u"ࠨࡲࡤࡷࡸࡽ࡯ࡳࡦࠪ⁓"): bstack11l11ll111l_opy_(cls.bs_config)
            })
        if bstack11l11l11_opy_.get(bstack11l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫ⁔")):
            os.environ[bstack11l1111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡈࡂࡕࡋࡉࡉࡥࡉࡅࠩ⁕")] = bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭⁖")]
        if bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⁗")].get(bstack11l1111_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ⁘"), {}).get(bstack11l1111_opy_ (u"ࠧࡢ࡮࡯ࡳࡼࡥࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ⁙")):
            os.environ[bstack11l1111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ⁚")] = str(bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⁛")][bstack11l1111_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ⁜")][bstack11l1111_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨ⁝")])
        else:
            os.environ[bstack11l1111_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡄࡐࡑࡕࡗࡠࡕࡆࡖࡊࡋࡎࡔࡊࡒࡘࡘ࠭⁞")] = bstack11l1111_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ ")
        return [bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠧ࡫ࡹࡷࠫ⁠")], bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ⁡")], os.environ[bstack11l1111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ⁢")]]
    @classmethod
    def bstack1lllll1ll111_opy_(cls, bstack11l11l11_opy_):
        if bstack11l11l11_opy_.get(bstack11l1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⁣")) == None:
            cls.bstack1lllll11ll11_opy_()
            return [None, None]
        if bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⁤")][bstack11l1111_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭⁥")] != True:
            cls.bstack1lllll11ll11_opy_(bstack11l11l11_opy_[bstack11l1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⁦")])
            return [None, None]
        if bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⁧")].get(bstack11l1111_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ⁨")):
            logger.debug(bstack11l1111_opy_ (u"ࠩࡗࡩࡸࡺࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭⁩"))
            parsed = json.loads(os.getenv(bstack11l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ⁪"), bstack11l1111_opy_ (u"ࠫࢀࢃࠧ⁫")))
            capabilities = bstack1ll1lll11_opy_.bstack1lllll1l11l1_opy_(bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⁬")][bstack11l1111_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧ⁭")][bstack11l1111_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭⁮")], bstack11l1111_opy_ (u"ࠨࡰࡤࡱࡪ࠭⁯"), bstack11l1111_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨ⁰"))
            bstack1llllll11111_opy_ = capabilities[bstack11l1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨⁱ")]
            os.environ[bstack11l1111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ⁲")] = bstack1llllll11111_opy_
            if bstack11l1111_opy_ (u"ࠧࡧࡵࡵࡱࡰࡥࡹ࡫ࠢ⁳") in bstack11l11l11_opy_ and bstack11l11l11_opy_.get(bstack11l1111_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ⁴")) is None:
                parsed[bstack11l1111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⁵")] = capabilities[bstack11l1111_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ⁶")]
            os.environ[bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ⁷")] = json.dumps(parsed)
            scripts = bstack1ll1lll11_opy_.bstack1lllll1l11l1_opy_(bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⁸")][bstack11l1111_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ⁹")][bstack11l1111_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭⁺")], bstack11l1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⁻"), bstack11l1111_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࠨ⁼"))
            bstack11llll1111_opy_.bstack11l1l1llll_opy_(scripts)
            commands = bstack11l11l11_opy_[bstack11l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⁽")][bstack11l1111_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ⁾")][bstack11l1111_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷ࡙ࡵࡗࡳࡣࡳࠫⁿ")].get(bstack11l1111_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭₀"))
            bstack11llll1111_opy_.bstack11l11llll1l_opy_(commands)
            bstack11l1l111lll_opy_ = capabilities.get(bstack11l1111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ₁"))
            bstack11llll1111_opy_.bstack11l11l11111_opy_(bstack11l1l111lll_opy_)
            bstack11llll1111_opy_.store()
        return [bstack1llllll11111_opy_, bstack11l11l11_opy_[bstack11l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨ₂")]]
    @classmethod
    def bstack1lllll1l1111_opy_(cls, response=None):
        os.environ[bstack11l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ₃")] = bstack11l1111_opy_ (u"ࠨࡰࡸࡰࡱ࠭₄")
        os.environ[bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭₅")] = bstack11l1111_opy_ (u"ࠪࡲࡺࡲ࡬ࠨ₆")
        os.environ[bstack11l1111_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡄࡑࡐࡔࡑࡋࡔࡆࡆࠪ₇")] = bstack11l1111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ₈")
        os.environ[bstack11l1111_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡋࡅࡘࡎࡅࡅࡡࡌࡈࠬ₉")] = bstack11l1111_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ₊")
        os.environ[bstack11l1111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ₋")] = bstack11l1111_opy_ (u"ࠤࡱࡹࡱࡲࠢ₌")
        cls.bstack1lllll11llll_opy_(response, bstack11l1111_opy_ (u"ࠥࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠥ₍"))
        return [None, None, None]
    @classmethod
    def bstack1lllll11ll11_opy_(cls, response=None):
        os.environ[bstack11l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ₎")] = bstack11l1111_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ₏")
        os.environ[bstack11l1111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫₐ")] = bstack11l1111_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬₑ")
        os.environ[bstack11l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬₒ")] = bstack11l1111_opy_ (u"ࠩࡱࡹࡱࡲࠧₓ")
        cls.bstack1lllll11llll_opy_(response, bstack11l1111_opy_ (u"ࠥࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠥₔ"))
        return [None, None, None]
    @classmethod
    def bstack1llllll1111l_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack11l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨₕ")] = jwt
        os.environ[bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪₖ")] = build_hashed_id
    @classmethod
    def bstack1lllll11llll_opy_(cls, response=None, product=bstack11l1111_opy_ (u"ࠨࠢₗ")):
        if response == None or response.get(bstack11l1111_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧₘ")) == None:
            logger.error(product + bstack11l1111_opy_ (u"ࠣࠢࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡪࡦ࡯࡬ࡦࡦࠥₙ"))
            return
        for error in response[bstack11l1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩₚ")]:
            bstack1111lll1ll1_opy_ = error[bstack11l1111_opy_ (u"ࠪ࡯ࡪࡿࠧₛ")]
            error_message = error[bstack11l1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬₜ")]
            if error_message:
                if bstack1111lll1ll1_opy_ == bstack11l1111_opy_ (u"ࠧࡋࡒࡓࡑࡕࡣࡆࡉࡃࡆࡕࡖࡣࡉࡋࡎࡊࡇࡇࠦ₝"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack11l1111_opy_ (u"ࠨࡄࡢࡶࡤࠤࡺࡶ࡬ࡰࡣࡧࠤࡹࡵࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࠢ₞") + product + bstack11l1111_opy_ (u"ࠢࠡࡨࡤ࡭ࡱ࡫ࡤࠡࡦࡸࡩࠥࡺ࡯ࠡࡵࡲࡱࡪࠦࡥࡳࡴࡲࡶࠧ₟"))
    @classmethod
    def bstack1lllll11ll1l_opy_(cls):
        if cls.bstack111111ll1ll_opy_ is not None:
            return
        cls.bstack111111ll1ll_opy_ = bstack111111lll1l_opy_(cls.bstack1lllll1l11ll_opy_)
        cls.bstack111111ll1ll_opy_.start()
    @classmethod
    def bstack111l1l1l1l_opy_(cls):
        if cls.bstack111111ll1ll_opy_ is None:
            return
        cls.bstack111111ll1ll_opy_.shutdown()
    @classmethod
    @bstack111l11l1l1_opy_(class_method=True)
    def bstack1lllll1l11ll_opy_(cls, bstack1111ll11ll_opy_, event_url=bstack11l1111_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡤࡸࡨ࡮ࠧ₠")):
        config = {
            bstack11l1111_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ₡"): cls.default_headers()
        }
        logger.debug(bstack11l1111_opy_ (u"ࠥࡴࡴࡹࡴࡠࡦࡤࡸࡦࡀࠠࡔࡧࡱࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡷࡩࡸࡺࡨࡶࡤࠣࡪࡴࡸࠠࡦࡸࡨࡲࡹࡹࠠࡼࡿࠥ₢").format(bstack11l1111_opy_ (u"ࠫ࠱ࠦࠧ₣").join([event[bstack11l1111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ₤")] for event in bstack1111ll11ll_opy_])))
        response = bstack1lllll1111_opy_(bstack11l1111_opy_ (u"࠭ࡐࡐࡕࡗࠫ₥"), cls.request_url(event_url), bstack1111ll11ll_opy_, config)
        bstack11l11l11l1l_opy_ = response.json()
    @classmethod
    def bstack1l1l11lll1_opy_(cls, bstack1111ll11ll_opy_, event_url=bstack11l1111_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭₦")):
        logger.debug(bstack11l1111_opy_ (u"ࠣࡵࡨࡲࡩࡥࡤࡢࡶࡤ࠾ࠥࡇࡴࡵࡧࡰࡴࡹ࡯࡮ࡨࠢࡷࡳࠥࡧࡤࡥࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ₧").format(bstack1111ll11ll_opy_[bstack11l1111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭₨")]))
        if not bstack1ll1lll11_opy_.bstack1lllll11l1ll_opy_(bstack1111ll11ll_opy_[bstack11l1111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ₩")]):
            logger.debug(bstack11l1111_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡐࡲࡸࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡪࡡࡵࡣࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ₪").format(bstack1111ll11ll_opy_[bstack11l1111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ₫")]))
            return
        bstack1l1l111lll_opy_ = bstack1ll1lll11_opy_.bstack1llllll111ll_opy_(bstack1111ll11ll_opy_[bstack11l1111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ€")], bstack1111ll11ll_opy_.get(bstack11l1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ₭")))
        if bstack1l1l111lll_opy_ != None:
            if bstack1111ll11ll_opy_.get(bstack11l1111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ₮")) != None:
                bstack1111ll11ll_opy_[bstack11l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ₯")][bstack11l1111_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ₰")] = bstack1l1l111lll_opy_
            else:
                bstack1111ll11ll_opy_[bstack11l1111_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ₱")] = bstack1l1l111lll_opy_
        if event_url == bstack11l1111_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫ₲"):
            cls.bstack1lllll11ll1l_opy_()
            logger.debug(bstack11l1111_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡶࡲࠤࡧࡧࡴࡤࡪࠣࡻ࡮ࡺࡨࠡࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ࠿ࠦࡻࡾࠤ₳").format(bstack1111ll11ll_opy_[bstack11l1111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ₴")]))
            cls.bstack111111ll1ll_opy_.add(bstack1111ll11ll_opy_)
        elif event_url == bstack11l1111_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭₵"):
            cls.bstack1lllll1l11ll_opy_([bstack1111ll11ll_opy_], event_url)
    @classmethod
    @bstack111l11l1l1_opy_(class_method=True)
    def bstack11lll11l_opy_(cls, logs):
        for log in logs:
            bstack1lllll1l1lll_opy_ = {
                bstack11l1111_opy_ (u"ࠩ࡮࡭ࡳࡪࠧ₶"): bstack11l1111_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡎࡒࡋࠬ₷"),
                bstack11l1111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ₸"): log[bstack11l1111_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ₹")],
                bstack11l1111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ₺"): log[bstack11l1111_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ₻")],
                bstack11l1111_opy_ (u"ࠨࡪࡷࡸࡵࡥࡲࡦࡵࡳࡳࡳࡹࡥࠨ₼"): {},
                bstack11l1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ₽"): log[bstack11l1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ₾")],
            }
            if bstack11l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ₿") in log:
                bstack1lllll1l1lll_opy_[bstack11l1111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⃀")] = log[bstack11l1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⃁")]
            elif bstack11l1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⃂") in log:
                bstack1lllll1l1lll_opy_[bstack11l1111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⃃")] = log[bstack11l1111_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⃄")]
            cls.bstack1l1l11lll1_opy_({
                bstack11l1111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⃅"): bstack11l1111_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⃆"),
                bstack11l1111_opy_ (u"ࠬࡲ࡯ࡨࡵࠪ⃇"): [bstack1lllll1l1lll_opy_]
            })
    @classmethod
    @bstack111l11l1l1_opy_(class_method=True)
    def bstack1lllll1l1l1l_opy_(cls, steps):
        bstack1lllll1llll1_opy_ = []
        for step in steps:
            bstack1lllll1ll11l_opy_ = {
                bstack11l1111_opy_ (u"࠭࡫ࡪࡰࡧࠫ⃈"): bstack11l1111_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡔࡆࡒࠪ⃉"),
                bstack11l1111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⃊"): step[bstack11l1111_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ⃋")],
                bstack11l1111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⃌"): step[bstack11l1111_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ⃍")],
                bstack11l1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⃎"): step[bstack11l1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ⃏")],
                bstack11l1111_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ⃐"): step[bstack11l1111_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪ⃑")]
            }
            if bstack11l1111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥ⃒ࠩ") in step:
                bstack1lllll1ll11l_opy_[bstack11l1111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦ⃓ࠪ")] = step[bstack11l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⃔")]
            elif bstack11l1111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⃕") in step:
                bstack1lllll1ll11l_opy_[bstack11l1111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⃖")] = step[bstack11l1111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ⃗")]
            bstack1lllll1llll1_opy_.append(bstack1lllll1ll11l_opy_)
        cls.bstack1l1l11lll1_opy_({
            bstack11l1111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩ⃘ࠬ"): bstack11l1111_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ⃙࠭"),
            bstack11l1111_opy_ (u"ࠪࡰࡴ࡭ࡳࠨ⃚"): bstack1lllll1llll1_opy_
        })
    @classmethod
    @bstack111l11l1l1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack1ll1111111_opy_, stage=STAGE.bstack1111llll1_opy_)
    def bstack1l111l1l_opy_(cls, screenshot):
        cls.bstack1l1l11lll1_opy_({
            bstack11l1111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ⃛"): bstack11l1111_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⃜"),
            bstack11l1111_opy_ (u"࠭࡬ࡰࡩࡶࠫ⃝"): [{
                bstack11l1111_opy_ (u"ࠧ࡬࡫ࡱࡨࠬ⃞"): bstack11l1111_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠪ⃟"),
                bstack11l1111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⃠"): datetime.datetime.utcnow().isoformat() + bstack11l1111_opy_ (u"ࠪ࡞ࠬ⃡"),
                bstack11l1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⃢"): screenshot[bstack11l1111_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫ⃣")],
                bstack11l1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⃤"): screenshot[bstack11l1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪ⃥ࠧ")]
            }]
        }, event_url=bstack11l1111_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ⃦࠭"))
    @classmethod
    @bstack111l11l1l1_opy_(class_method=True)
    def bstack1l11ll11l_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack1l1l11lll1_opy_({
            bstack11l1111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭⃧"): bstack11l1111_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪ⃨ࠧ"),
            bstack11l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭⃩"): {
                bstack11l1111_opy_ (u"ࠧࡻࡵࡪࡦ⃪ࠥ"): cls.current_test_uuid(),
                bstack11l1111_opy_ (u"ࠨࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷ⃫ࠧ"): cls.bstack111lll1l11_opy_(driver)
            }
        })
    @classmethod
    def bstack111ll111ll_opy_(cls, event: str, bstack1111ll11ll_opy_: bstack111l11lll1_opy_):
        bstack111l11l11l_opy_ = {
            bstack11l1111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ⃬ࠫ"): event,
            bstack1111ll11ll_opy_.bstack1111llllll_opy_(): bstack1111ll11ll_opy_.bstack111l111l1l_opy_(event)
        }
        cls.bstack1l1l11lll1_opy_(bstack111l11l11l_opy_)
        result = getattr(bstack1111ll11ll_opy_, bstack11l1111_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨ⃭"), None)
        if event == bstack11l1111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦ⃮ࠪ"):
            threading.current_thread().bstackTestMeta = {bstack11l1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵ⃯ࠪ"): bstack11l1111_opy_ (u"ࠫࡵ࡫࡮ࡥ࡫ࡱ࡫ࠬ⃰")}
        elif event == bstack11l1111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⃱"):
            threading.current_thread().bstackTestMeta = {bstack11l1111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭⃲"): getattr(result, bstack11l1111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⃳"), bstack11l1111_opy_ (u"ࠨࠩ⃴"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⃵"), None) is None or os.environ[bstack11l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ⃶")] == bstack11l1111_opy_ (u"ࠦࡳࡻ࡬࡭ࠤ⃷")) and (os.environ.get(bstack11l1111_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ⃸"), None) is None or os.environ[bstack11l1111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ⃹")] == bstack11l1111_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ⃺")):
            return False
        return True
    @staticmethod
    def bstack1lllll1ll1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack111lll111_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack11l1111_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ⃻"): bstack11l1111_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ⃼"),
            bstack11l1111_opy_ (u"ࠪ࡜࠲ࡈࡓࡕࡃࡆࡏ࠲࡚ࡅࡔࡖࡒࡔࡘ࠭⃽"): bstack11l1111_opy_ (u"ࠫࡹࡸࡵࡦࠩ⃾")
        }
        if os.environ.get(bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ⃿"), None):
            headers[bstack11l1111_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭℀")] = bstack11l1111_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࡼࡿࠪ℁").format(os.environ[bstack11l1111_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠧℂ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack11l1111_opy_ (u"ࠩࡾࢁ࠴ࢁࡽࠨ℃").format(bstack1lllll11lll1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack11l1111_opy_ (u"ࠪࡧࡺࡸࡲࡦࡰࡷࡣࡹ࡫ࡳࡵࡡࡸࡹ࡮ࡪࠧ℄"), None)
    @staticmethod
    def bstack111lll1l11_opy_(driver):
        return {
            bstack111ll11l111_opy_(): bstack111l1111l1l_opy_(driver)
        }
    @staticmethod
    def bstack1lllll1l1ll1_opy_(exception_info, report):
        return [{bstack11l1111_opy_ (u"ࠫࡧࡧࡣ࡬ࡶࡵࡥࡨ࡫ࠧ℅"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack111111llll_opy_(typename):
        if bstack11l1111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࠣ℆") in typename:
            return bstack11l1111_opy_ (u"ࠨࡁࡴࡵࡨࡶࡹ࡯࡯࡯ࡇࡵࡶࡴࡸࠢℇ")
        return bstack11l1111_opy_ (u"ࠢࡖࡰ࡫ࡥࡳࡪ࡬ࡦࡦࡈࡶࡷࡵࡲࠣ℈")