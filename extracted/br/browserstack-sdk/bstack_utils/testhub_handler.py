# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11l111111ll_opy_, bstack111llll11l1_opy_, bstack11111l1l_opy_, error_handler, bstack111lll1ll11_opy_, bstack111ll11ll11_opy_, bstack111l111ll11_opy_, current_time, bstack11llll11l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1llll111l11l_opy_ import bstack1llll1111lll_opy_
import bstack_utils.bstack1ll1l1l1ll_opy_ as TestHubUtils
from bstack_utils.bstack11l1llll_opy_ import bstack11l1ll1111_opy_
import bstack_utils.accessibility as bstack1ll11lll11_opy_
from bstack_utils.bstack1l1l1l1lll_opy_ import bstack1l1l1l1lll_opy_
from bstack_utils.test_data import bstack1lllll1ll11_opy_
from bstack_utils.constants import bstack11llll1l1_opy_
bstack1lll11ll11ll_opy_ = bstack1ll111_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡤࡱ࡯ࡰࡪࡩࡴࡰࡴ࠰ࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ᾆ")
logger = logging.getLogger(__name__)
class TestHubHandler:
    bstack1llll111l11l_opy_ = None
    bs_config = None
    bstack11111l1ll_opy_ = None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1lll1l111ll1_opy_, stage=STAGE.bstack11ll1111_opy_)
    def launch(cls, bs_config, bstack11111l1ll_opy_):
        cls.bs_config = bs_config
        cls.bstack11111l1ll_opy_ = bstack11111l1ll_opy_
        try:
            cls.bstack1lll1l11111l_opy_()
            bstack1lll1l1111ll_opy_ = bstack11l111111ll_opy_(bs_config)
            bstack1lll11ll1lll_opy_ = bstack111llll11l1_opy_(bs_config)
            data = TestHubUtils.bstack1lll11ll1l1l_opy_(bs_config, bstack11111l1ll_opy_)
            config = {
                bstack1ll111_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᾇ"): (bstack1lll1l1111ll_opy_, bstack1lll11ll1lll_opy_),
                bstack1ll111_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᾈ"): cls.default_headers()
            }
            response = bstack11111l1l_opy_(bstack1ll111_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᾉ"), cls.request_url(bstack1ll111_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠴࠲ࡦࡺ࡯࡬ࡥࡵࠪᾊ")), data, config)
            if response.status_code != 200:
                bstack1ll11ll11l_opy_ = response.json()
                if bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᾋ")] == False:
                    cls.bstack1lll11lll111_opy_(bstack1ll11ll11l_opy_)
                    return
                cls.bstack1lll11l1ll11_opy_(bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᾌ")])
                cls.bstack1lll1l11l111_opy_(bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᾍ")])
                return None
            bstack1lll1l111l1l_opy_ = cls.bstack1lll11lll11l_opy_(response)
            return bstack1lll1l111l1l_opy_, response.json()
        except Exception as error:
            logger.error(bstack1ll111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡧࡻࡩ࡭ࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡾࢁࠧᾎ").format(str(error)))
            return None
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1lll11llll11_opy_, stage=STAGE.bstack11ll1111_opy_)
    def stop(cls, bstack1lll1l11l11l_opy_=None):
        if not bstack11l1ll1111_opy_.on() and not bstack1ll11lll11_opy_.on():
            return
        if os.environ.get(bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᾏ")) == bstack1ll111_opy_ (u"ࠤࡱࡹࡱࡲࠢᾐ") or os.environ.get(bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᾑ")) == bstack1ll111_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᾒ"):
            logger.error(bstack1ll111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᾓ"))
            return {
                bstack1ll111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᾔ"): bstack1ll111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᾕ"),
                bstack1ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᾖ"): bstack1ll111_opy_ (u"ࠩࡗࡳࡰ࡫࡮࠰ࡤࡸ࡭ࡱࡪࡉࡅࠢ࡬ࡷࠥࡻ࡮ࡥࡧࡩ࡭ࡳ࡫ࡤ࠭ࠢࡥࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣࡱ࡮࡭ࡨࡵࠢ࡫ࡥࡻ࡫ࠠࡧࡣ࡬ࡰࡪࡪࠧᾗ")
            }
        try:
            cls.bstack1llll111l11l_opy_.shutdown()
            data = {
                bstack1ll111_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡧࡴࠨᾘ"): current_time()
            }
            if not bstack1lll1l11l11l_opy_ is None:
                data[bstack1ll111_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥ࡭ࡦࡶࡤࡨࡦࡺࡡࠨᾙ")] = [{
                    bstack1ll111_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᾚ"): bstack1ll111_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫᾛ"),
                    bstack1ll111_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧᾜ"): bstack1lll1l11l11l_opy_
                }]
            config = {
                bstack1ll111_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᾝ"): cls.default_headers()
            }
            bstack11111llllll_opy_ = bstack1ll111_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡹ࡮ࡲࡤࡴ࠱ࡾࢁ࠴ࡹࡴࡰࡲࠪᾞ").format(os.environ[bstack1ll111_opy_ (u"ࠥࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠣᾟ")])
            bstack1lll11l1ll1l_opy_ = cls.request_url(bstack11111llllll_opy_)
            response = bstack11111l1l_opy_(bstack1ll111_opy_ (u"ࠫࡕ࡛ࡔࠨᾠ"), bstack1lll11l1ll1l_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1ll111_opy_ (u"࡙ࠧࡴࡰࡲࠣࡶࡪࡷࡵࡦࡵࡷࠤࡳࡵࡴࠡࡱ࡮ࠦᾡ"))
        except Exception as error:
            logger.error(bstack1ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡰࡲࠣࡦࡺ࡯࡬ࡥࠢࡵࡩࡶࡻࡥࡴࡶࠣࡸࡴࠦࡔࡦࡵࡷࡌࡺࡨ࠺࠻ࠢࠥᾢ") + str(error))
            return {
                bstack1ll111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᾣ"): bstack1ll111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᾤ"),
                bstack1ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᾥ"): str(error)
            }
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll11lll11l_opy_(cls, response):
        bstack1ll11ll11l_opy_ = response.json() if not isinstance(response, dict) else response
        bstack1lll1l111l1l_opy_ = {}
        if bstack1ll11ll11l_opy_.get(bstack1ll111_opy_ (u"ࠪ࡮ࡼࡺࠧᾦ")) is None:
            os.environ[bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᾧ")] = bstack1ll111_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᾨ")
        else:
            os.environ[bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪᾩ")] = bstack1ll11ll11l_opy_.get(bstack1ll111_opy_ (u"ࠧ࡫ࡹࡷࠫᾪ"), bstack1ll111_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᾫ"))
        os.environ[bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᾬ")] = bstack1ll11ll11l_opy_.get(bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᾭ"), bstack1ll111_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᾮ"))
        logger.info(bstack1ll111_opy_ (u"࡚ࠬࡥࡴࡶ࡫ࡹࡧࠦࡳࡵࡣࡵࡸࡪࡪࠠࡸ࡫ࡷ࡬ࠥ࡯ࡤ࠻ࠢࠪᾯ") + os.getenv(bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᾰ")));
        if bstack11l1ll1111_opy_.bstack1lll11l1l1ll_opy_(cls.bs_config, cls.bstack11111l1ll_opy_.get(bstack1ll111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨᾱ"), bstack1ll111_opy_ (u"ࠨࠩᾲ"))) is True:
            bstack1lll1llll1l1_opy_, build_hashed_id, allow_screenshots = cls.bstack1lll11ll1ll1_opy_(bstack1ll11ll11l_opy_)
            if bstack1lll1llll1l1_opy_ != None and build_hashed_id != None:
                bstack1lll1l111l1l_opy_[bstack1ll111_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᾳ")] = {
                    bstack1ll111_opy_ (u"ࠪ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳ࠭ᾴ"): bstack1lll1llll1l1_opy_,
                    bstack1ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭᾵"): build_hashed_id,
                    bstack1ll111_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᾶ"): allow_screenshots
                }
            else:
                bstack1lll1l111l1l_opy_[bstack1ll111_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᾷ")] = {}
        else:
            bstack1lll1l111l1l_opy_[bstack1ll111_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᾸ")] = {}
        bstack1lll1l11l1l1_opy_, build_hashed_id = cls.bstack1lll11ll11l1_opy_(bstack1ll11ll11l_opy_)
        if bstack1lll1l11l1l1_opy_ != None and build_hashed_id != None:
            bstack1lll1l111l1l_opy_[bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᾹ")] = {
                bstack1ll111_opy_ (u"ࠩࡤࡹࡹ࡮࡟ࡵࡱ࡮ࡩࡳ࠭Ὰ"): bstack1lll1l11l1l1_opy_,
                bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬΆ"): build_hashed_id,
            }
        else:
            bstack1lll1l111l1l_opy_[bstack1ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᾼ")] = {}
        if bstack1lll1l111l1l_opy_[bstack1ll111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ᾽")].get(bstack1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨι")) != None or bstack1lll1l111l1l_opy_[bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᾿")].get(bstack1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ῀")) != None:
            cls.bstack1lll11llllll_opy_(bstack1ll11ll11l_opy_.get(bstack1ll111_opy_ (u"ࠩ࡭ࡻࡹ࠭῁")), bstack1ll11ll11l_opy_.get(bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬῂ")))
        return bstack1lll1l111l1l_opy_
    @classmethod
    def bstack1lll11ll1ll1_opy_(cls, bstack1ll11ll11l_opy_):
        if bstack1ll11ll11l_opy_.get(bstack1ll111_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫῃ")) == None:
            cls.bstack1lll11l1ll11_opy_()
            return [None, None, None]
        if bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬῄ")][bstack1ll111_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ῅")] != True:
            cls.bstack1lll11l1ll11_opy_(bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧῆ")])
            return [None, None, None]
        logger.debug(bstack1ll111_opy_ (u"ࠨࡽࢀࠤࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲ࡙ࠥࡵࡤࡥࡨࡷࡸ࡬ࡵ࡭ࠣࠪῇ").format(bstack11llll1l1_opy_))
        os.environ[bstack1ll111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨῈ")] = bstack1ll111_opy_ (u"ࠪࡸࡷࡻࡥࠨΈ")
        if bstack1ll11ll11l_opy_.get(bstack1ll111_opy_ (u"ࠫ࡯ࡽࡴࠨῊ")):
            os.environ[bstack1ll111_opy_ (u"ࠬࡉࡒࡆࡆࡈࡒ࡙ࡏࡁࡍࡕࡢࡊࡔࡘ࡟ࡄࡔࡄࡗࡍࡥࡒࡆࡒࡒࡖ࡙ࡏࡎࡈࠩΉ")] = json.dumps({
                bstack1ll111_opy_ (u"࠭ࡵࡴࡧࡵࡲࡦࡳࡥࠨῌ"): bstack11l111111ll_opy_(cls.bs_config),
                bstack1ll111_opy_ (u"ࠧࡱࡣࡶࡷࡼࡵࡲࡥࠩ῍"): bstack111llll11l1_opy_(cls.bs_config)
            })
        if bstack1ll11ll11l_opy_.get(bstack1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ῎")):
            os.environ[bstack1ll111_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡎࡁࡔࡊࡈࡈࡤࡏࡄࠨ῏")] = bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬῐ")]
        if bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫῑ")].get(bstack1ll111_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ῒ"), {}).get(bstack1ll111_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪΐ")):
            os.environ[bstack1ll111_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ῔")] = str(bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ῕")][bstack1ll111_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪῖ")][bstack1ll111_opy_ (u"ࠪࡥࡱࡲ࡯ࡸࡡࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧῗ")])
        else:
            os.environ[bstack1ll111_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡃࡏࡐࡔ࡝࡟ࡔࡅࡕࡉࡊࡔࡓࡉࡑࡗࡗࠬῘ")] = bstack1ll111_opy_ (u"ࠧࡴࡵ࡭࡮ࠥῙ")
        return [bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"࠭ࡪࡸࡶࠪῚ")], bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩΊ")], os.environ[bstack1ll111_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡇࡌࡍࡑ࡚ࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࡔࠩ῜")]]
    @classmethod
    def bstack1lll11ll11l1_opy_(cls, bstack1ll11ll11l_opy_):
        if bstack1ll11ll11l_opy_.get(bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ῝")) == None:
            cls.bstack1lll1l11l111_opy_()
            return [None, None]
        if bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ῞")][bstack1ll111_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬ῟")] != True:
            cls.bstack1lll1l11l111_opy_(bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬῠ")])
            return [None, None]
        if bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ῡ")].get(bstack1ll111_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨῢ")):
            logger.debug(bstack1ll111_opy_ (u"ࠨࡖࡨࡷࡹࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡔࡷࡦࡧࡪࡹࡳࡧࡷ࡯ࠥࠬΰ"))
            parsed = json.loads(os.getenv(bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪῤ"), bstack1ll111_opy_ (u"ࠪࡿࢂ࠭ῥ")))
            capabilities = TestHubUtils.bstack1lll11lllll1_opy_(bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫῦ")][bstack1ll111_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ῧ")][bstack1ll111_opy_ (u"࠭ࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬῨ")], bstack1ll111_opy_ (u"ࠧ࡯ࡣࡰࡩࠬῩ"), bstack1ll111_opy_ (u"ࠨࡸࡤࡰࡺ࡫ࠧῪ"))
            bstack1lll1l11l1l1_opy_ = capabilities[bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧΎ")]
            os.environ[bstack1ll111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨῬ")] = bstack1lll1l11l1l1_opy_
            if bstack1ll111_opy_ (u"ࠦࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ῭") in bstack1ll11ll11l_opy_ and bstack1ll11ll11l_opy_.get(bstack1ll111_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦ΅")) is None:
                parsed[bstack1ll111_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ`")] = capabilities[bstack1ll111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ῰")]
            os.environ[bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ῱")] = json.dumps(parsed)
            scripts = TestHubUtils.bstack1lll11lllll1_opy_(bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩῲ")][bstack1ll111_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫῳ")][bstack1ll111_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬῴ")], bstack1ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ῵"), bstack1ll111_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࠧῶ"))
            bstack1l1l1l1lll_opy_.bstack1lllll1l1_opy_(scripts)
            commands = bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧῷ")][bstack1ll111_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩῸ")][bstack1ll111_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࡘࡴ࡝ࡲࡢࡲࠪΌ")].get(bstack1ll111_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬῺ"))
            bstack1l1l1l1lll_opy_.bstack1lll11lll1ll_opy_(commands)
            bstack1lll11ll111l_opy_ = capabilities.get(bstack1ll111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩΏ"))
            bstack1l1l1l1lll_opy_.bstack1lll11l1lll1_opy_(bstack1lll11ll111l_opy_)
            bstack1l1l1l1lll_opy_.store()
        return [bstack1lll1l11l1l1_opy_, bstack1ll11ll11l_opy_[bstack1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧῼ")]]
    @classmethod
    def bstack1lll11l1ll11_opy_(cls, response=None):
        os.environ[bstack1ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ´")] = bstack1ll111_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ῾")
        os.environ[bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ῿")] = bstack1ll111_opy_ (u"ࠩࡱࡹࡱࡲࠧ ")
        os.environ[bstack1ll111_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩ ")] = bstack1ll111_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ ")
        os.environ[bstack1ll111_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫ ")] = bstack1ll111_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ ")
        os.environ[bstack1ll111_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨ ")] = bstack1ll111_opy_ (u"ࠣࡰࡸࡰࡱࠨ ")
        cls.bstack1lll11lll111_opy_(response, bstack1ll111_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤ "))
        return [None, None, None]
    @classmethod
    def bstack1lll1l11l111_opy_(cls, response=None):
        os.environ[bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ ")] = bstack1ll111_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ ")
        os.environ[bstack1ll111_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ ")] = bstack1ll111_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ​")
        os.environ[bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ‌")] = bstack1ll111_opy_ (u"ࠨࡰࡸࡰࡱ࠭‍")
        cls.bstack1lll11lll111_opy_(response, bstack1ll111_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤ‎"))
        return [None, None, None]
    @classmethod
    def bstack1lll11llllll_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ‏")] = jwt
        os.environ[bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ‐")] = build_hashed_id
    @classmethod
    def bstack1lll11lll111_opy_(cls, response=None, product=bstack1ll111_opy_ (u"ࠧࠨ‑")):
        if response == None or response.get(bstack1ll111_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭‒")) == None:
            logger.error(product + bstack1ll111_opy_ (u"ࠢࠡࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠤ–"))
            return
        for error in response[bstack1ll111_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨ—")]:
            bstack111llllllll_opy_ = error[bstack1ll111_opy_ (u"ࠩ࡮ࡩࡾ࠭―")]
            error_message = error[bstack1ll111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ‖")]
            if error_message:
                if bstack111llllllll_opy_ == bstack1ll111_opy_ (u"ࠦࡊࡘࡒࡐࡔࡢࡅࡈࡉࡅࡔࡕࡢࡈࡊࡔࡉࡆࡆࠥ‗"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1ll111_opy_ (u"ࠧࡊࡡࡵࡣࠣࡹࡵࡲ࡯ࡢࡦࠣࡸࡴࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࠨ‘") + product + bstack1ll111_opy_ (u"ࠨࠠࡧࡣ࡬ࡰࡪࡪࠠࡥࡷࡨࠤࡹࡵࠠࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦ’"))
    @classmethod
    def bstack1lll1l11111l_opy_(cls):
        if cls.bstack1llll111l11l_opy_ is not None:
            return
        cls.bstack1llll111l11l_opy_ = bstack1llll1111lll_opy_(cls.post_data)
        cls.bstack1llll111l11l_opy_.start()
    @classmethod
    def bstack1lllll111ll_opy_(cls):
        if cls.bstack1llll111l11l_opy_ is None:
            return
        cls.bstack1llll111l11l_opy_.shutdown()
    @classmethod
    @error_handler(class_method=True)
    def post_data(cls, bstack1lllll111l1_opy_, event_url=bstack1ll111_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭‚")):
        config = {
            bstack1ll111_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ‛"): cls.default_headers()
        }
        logger.debug(bstack1ll111_opy_ (u"ࠤࡳࡳࡸࡺ࡟ࡥࡣࡷࡥ࠿ࠦࡓࡦࡰࡧ࡭ࡳ࡭ࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡶࡨࡷࡹ࡮ࡵࡣࠢࡩࡳࡷࠦࡥࡷࡧࡱࡸࡸࠦࡻࡾࠤ“").format(bstack1ll111_opy_ (u"ࠪ࠰ࠥ࠭”").join([event[bstack1ll111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ„")] for event in bstack1lllll111l1_opy_])))
        response = bstack11111l1l_opy_(bstack1ll111_opy_ (u"ࠬࡖࡏࡔࡖࠪ‟"), cls.request_url(event_url), bstack1lllll111l1_opy_, config)
        bstack1lll1l1111l1_opy_ = response.json()
    @classmethod
    def bstack111l1lll11_opy_(cls, bstack1lllll111l1_opy_, event_url=bstack1ll111_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬ†")):
        logger.debug(bstack1ll111_opy_ (u"ࠢࡴࡧࡱࡨࡤࡪࡡࡵࡣ࠽ࠤࡆࡺࡴࡦ࡯ࡳࡸ࡮ࡴࡧࠡࡶࡲࠤࡦࡪࡤࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ‡").format(bstack1lllll111l1_opy_[bstack1ll111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ•")]))
        if not TestHubUtils.bstack1lll11ll1l11_opy_(bstack1lllll111l1_opy_[bstack1ll111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭‣")]):
            logger.debug(bstack1ll111_opy_ (u"ࠥࡷࡪࡴࡤࡠࡦࡤࡸࡦࡀࠠࡏࡱࡷࠤࡦࡪࡤࡪࡰࡪࠤࡩࡧࡴࡢࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ․").format(bstack1lllll111l1_opy_[bstack1ll111_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ‥")]))
            return
        bstack1ll11l1l11_opy_ = TestHubUtils.bstack1lll1l111lll_opy_(bstack1lllll111l1_opy_[bstack1ll111_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ…")], bstack1lllll111l1_opy_.get(bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨ‧")))
        if bstack1ll11l1l11_opy_ != None:
            if bstack1lllll111l1_opy_.get(bstack1ll111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩ ")) != None:
                bstack1lllll111l1_opy_[bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࠪ ")][bstack1ll111_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ‪")] = bstack1ll11l1l11_opy_
            else:
                bstack1lllll111l1_opy_[bstack1ll111_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ‫")] = bstack1ll11l1l11_opy_
        if event_url == bstack1ll111_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡧࡴࡤࡪࠪ‬"):
            cls.bstack1lll1l11111l_opy_()
            logger.debug(bstack1ll111_opy_ (u"ࠧࡹࡥ࡯ࡦࡢࡨࡦࡺࡡ࠻ࠢࡄࡨࡩ࡯࡮ࡨࠢࡧࡥࡹࡧࠠࡵࡱࠣࡦࡦࡺࡣࡩࠢࡺ࡭ࡹ࡮ࠠࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨ࠾ࠥࢁࡽࠣ‭").format(bstack1lllll111l1_opy_[bstack1ll111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ‮")]))
            cls.bstack1llll111l11l_opy_.add(bstack1lllll111l1_opy_)
        elif event_url == bstack1ll111_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ "):
            cls.post_data([bstack1lllll111l1_opy_], event_url)
    @classmethod
    @error_handler(class_method=True)
    def bstack11lll1l1_opy_(cls, logs):
        for log in logs:
            bstack1lll11llll1l_opy_ = {
                bstack1ll111_opy_ (u"ࠨ࡭࡬ࡲࡩ࠭‰"): bstack1ll111_opy_ (u"ࠩࡗࡉࡘ࡚࡟ࡍࡑࡊࠫ‱"),
                bstack1ll111_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ′"): log[bstack1ll111_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪ″")],
                bstack1ll111_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ‴"): log[bstack1ll111_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩ‵")],
                bstack1ll111_opy_ (u"ࠧࡩࡶࡷࡴࡤࡸࡥࡴࡲࡲࡲࡸ࡫ࠧ‶"): {},
                bstack1ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ‷"): log[bstack1ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ‸")],
            }
            if bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ‹") in log:
                bstack1lll11llll1l_opy_[bstack1ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ›")] = log[bstack1ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ※")]
            elif bstack1ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭‼") in log:
                bstack1lll11llll1l_opy_[bstack1ll111_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ‽")] = log[bstack1ll111_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ‾")]
            cls.bstack111l1lll11_opy_({
                bstack1ll111_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭‿"): bstack1ll111_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⁀"),
                bstack1ll111_opy_ (u"ࠫࡱࡵࡧࡴࠩ⁁"): [bstack1lll11llll1l_opy_]
            })
    @classmethod
    @error_handler(class_method=True)
    def bstack1lll1l111l11_opy_(cls, steps):
        bstack1lll11l1llll_opy_ = []
        for step in steps:
            bstack1lll11ll1111_opy_ = {
                bstack1ll111_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ⁂"): bstack1ll111_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘ࡚ࡅࡑࠩ⁃"),
                bstack1ll111_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭⁄"): step[bstack1ll111_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ⁅")],
                bstack1ll111_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ⁆"): step[bstack1ll111_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭⁇")],
                bstack1ll111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⁈"): step[bstack1ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭⁉")],
                bstack1ll111_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ⁊"): step[bstack1ll111_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ⁋")]
            }
            if bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ⁌") in step:
                bstack1lll11ll1111_opy_[bstack1ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ⁍")] = step[bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ⁎")]
            elif bstack1ll111_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ⁏") in step:
                bstack1lll11ll1111_opy_[bstack1ll111_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⁐")] = step[bstack1ll111_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭⁑")]
            bstack1lll11l1llll_opy_.append(bstack1lll11ll1111_opy_)
        cls.bstack111l1lll11_opy_({
            bstack1ll111_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ⁒"): bstack1ll111_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⁓"),
            bstack1ll111_opy_ (u"ࠩ࡯ࡳ࡬ࡹࠧ⁔"): bstack1lll11l1llll_opy_
        })
    @classmethod
    @error_handler(class_method=True)
    @measure(event_name=EVENTS.bstack1l11l111l1_opy_, stage=STAGE.bstack11ll1111_opy_)
    def bstack11ll11111l_opy_(cls, screenshot):
        cls.bstack111l1lll11_opy_({
            bstack1ll111_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ⁕"): bstack1ll111_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⁖"),
            bstack1ll111_opy_ (u"ࠬࡲ࡯ࡨࡵࠪ⁗"): [{
                bstack1ll111_opy_ (u"࠭࡫ࡪࡰࡧࠫ⁘"): bstack1ll111_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࠩ⁙"),
                bstack1ll111_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ⁚"): datetime.datetime.utcnow().isoformat() + bstack1ll111_opy_ (u"ࠩ࡝ࠫ⁛"),
                bstack1ll111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⁜"): screenshot[bstack1ll111_opy_ (u"ࠫ࡮ࡳࡡࡨࡧࠪ⁝")],
                bstack1ll111_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ⁞"): screenshot[bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ ")]
            }]
        }, event_url=bstack1ll111_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࡷࠬ⁠"))
    @classmethod
    @error_handler(class_method=True)
    def send_cbt_info(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack111l1lll11_opy_({
            bstack1ll111_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ⁡"): bstack1ll111_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭⁢"),
            bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬ⁣"): {
                bstack1ll111_opy_ (u"ࠦࡺࡻࡩࡥࠤ⁤"): cls.current_test_uuid(),
                bstack1ll111_opy_ (u"ࠧ࡯࡮ࡵࡧࡪࡶࡦࡺࡩࡰࡰࡶࠦ⁥"): cls.bstack11111l111l_opy_(driver)
            }
        })
    @classmethod
    def send_run_event(cls, event: str, bstack1lllll111l1_opy_: bstack1lllll1ll11_opy_):
        bstack1lllll1llll_opy_ = {
            bstack1ll111_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ⁦"): event,
            bstack1lllll111l1_opy_.bstack1111111ll1_opy_(): bstack1lllll111l1_opy_.bstack111111l11l_opy_(event)
        }
        cls.bstack111l1lll11_opy_(bstack1lllll1llll_opy_)
        result = getattr(bstack1lllll111l1_opy_, bstack1ll111_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧ⁧"), None)
        if event == bstack1ll111_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⁨"):
            threading.current_thread().bstackTestMeta = {bstack1ll111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⁩"): bstack1ll111_opy_ (u"ࠪࡴࡪࡴࡤࡪࡰࡪࠫ⁪")}
        elif event == bstack1ll111_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⁫"):
            threading.current_thread().bstackTestMeta = {bstack1ll111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ⁬"): getattr(result, bstack1ll111_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭⁭"), bstack1ll111_opy_ (u"ࠧࠨ⁮"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ⁯"), None) is None or os.environ[bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭⁰")] == bstack1ll111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣⁱ")) and (os.environ.get(bstack1ll111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ⁲"), None) is None or os.environ[bstack1ll111_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ⁳")] == bstack1ll111_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦ⁴")):
            return False
        return True
    @staticmethod
    def bstack1lll1l111111_opy_(func):
        def wrap(*args, **kwargs):
            if TestHubHandler.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1ll111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭⁵"): bstack1ll111_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ⁶"),
            bstack1ll111_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬ⁷"): bstack1ll111_opy_ (u"ࠪࡸࡷࡻࡥࠨ⁸")
        }
        if os.environ.get(bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ⁹"), None):
            headers[bstack1ll111_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ⁺")] = bstack1ll111_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩ⁻").format(os.environ[bstack1ll111_opy_ (u"ࠢࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠦ⁼")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1ll111_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧ⁽").format(bstack1lll11ll11ll_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1ll111_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭⁾"), None)
    @staticmethod
    def bstack11111l111l_opy_(driver):
        return {
            bstack111lll1ll11_opy_(): bstack111ll11ll11_opy_(driver)
        }
    @staticmethod
    def bstack1lll11lll1l1_opy_(exception_info, report):
        return [{bstack1ll111_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ⁿ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack1lll11ll1l1_opy_(typename):
        if bstack1ll111_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢ₀") in typename:
            return bstack1ll111_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨ₁")
        return bstack1ll111_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢ₂")