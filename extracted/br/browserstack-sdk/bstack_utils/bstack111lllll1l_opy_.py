# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import json
import logging
import os
import datetime
import threading
from bstack_utils.constants import EVENTS, STAGE
from bstack_utils.helper import bstack11lll111111_opy_, bstack11llll111ll_opy_, bstack1l1ll1l111_opy_, bstack111l1ll1l1_opy_, bstack11l1l1ll1ll_opy_, bstack11l1l11lll1_opy_, bstack11l111111ll_opy_, bstack1llllllll1_opy_, bstack1ll11l1l1l_opy_
from bstack_utils.measure import measure
from bstack_utils.bstack1111l1l111l_opy_ import bstack1111l1l11ll_opy_
import bstack_utils.bstack11l111lll_opy_ as bstack1lll1l1l_opy_
from bstack_utils.bstack111lll1l1l_opy_ import bstack11l1ll111_opy_
import bstack_utils.accessibility as bstack1l11l11ll1_opy_
from bstack_utils.bstack11ll1l1ll_opy_ import bstack11ll1l1ll_opy_
from bstack_utils.bstack11l111111l_opy_ import bstack111l1l1111_opy_
bstack111111l1l11_opy_ = bstack111lll_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡣࡰ࡮࡯ࡩࡨࡺ࡯ࡳ࠯ࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬἿ")
logger = logging.getLogger(__name__)
class bstack11111ll1l_opy_:
    bstack1111l1l111l_opy_ = None
    bs_config = None
    bstack1ll1l11l1l_opy_ = None
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11ll11l1111_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def launch(cls, bs_config, bstack1ll1l11l1l_opy_):
        cls.bs_config = bs_config
        cls.bstack1ll1l11l1l_opy_ = bstack1ll1l11l1l_opy_
        try:
            cls.bstack11111l1l1ll_opy_()
            bstack11lll1l1111_opy_ = bstack11lll111111_opy_(bs_config)
            bstack11llll111l1_opy_ = bstack11llll111ll_opy_(bs_config)
            data = bstack1lll1l1l_opy_.bstack11111l11l11_opy_(bs_config, bstack1ll1l11l1l_opy_)
            config = {
                bstack111lll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫὀ"): (bstack11lll1l1111_opy_, bstack11llll111l1_opy_),
                bstack111lll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨὁ"): cls.default_headers()
            }
            response = bstack1l1ll1l111_opy_(bstack111lll_opy_ (u"ࠨࡒࡒࡗ࡙࠭ὂ"), cls.request_url(bstack111lll_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠳࠱ࡥࡹ࡮ࡲࡤࡴࠩὃ")), data, config)
            if response.status_code != 200:
                bstack1111l1ll1_opy_ = response.json()
                if bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫὄ")] == False:
                    cls.bstack111111l1lll_opy_(bstack1111l1ll1_opy_)
                    return
                cls.bstack111111ll11l_opy_(bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫὅ")])
                cls.bstack111111l1l1l_opy_(bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ὆")])
                return None
            bstack111111l11ll_opy_ = cls.bstack111111ll111_opy_(response)
            return bstack111111l11ll_opy_, response.json()
        except Exception as error:
            logger.error(bstack111lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡦࡺ࡯࡬ࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࡽࢀࠦ὇").format(str(error)))
            return None
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    def stop(cls, bstack11111l11111_opy_=None):
        if not bstack11l1ll111_opy_.on() and not bstack1l11l11ll1_opy_.on():
            return
        if os.environ.get(bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫὈ")) == bstack111lll_opy_ (u"ࠣࡰࡸࡰࡱࠨὉ") or os.environ.get(bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧὊ")) == bstack111lll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣὋ"):
            logger.error(bstack111lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡵࡰࠡࡤࡸ࡭ࡱࡪࠠࡳࡧࡴࡹࡪࡹࡴࠡࡶࡲࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧὌ"))
            return {
                bstack111lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬὍ"): bstack111lll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬ὎"),
                bstack111lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ὏"): bstack111lll_opy_ (u"ࠨࡖࡲ࡯ࡪࡴ࠯ࡣࡷ࡬ࡰࡩࡏࡄࠡ࡫ࡶࠤࡺࡴࡤࡦࡨ࡬ࡲࡪࡪࠬࠡࡤࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢࡰ࡭࡬࡮ࡴࠡࡪࡤࡺࡪࠦࡦࡢ࡫࡯ࡩࡩ࠭ὐ")
            }
        try:
            cls.bstack1111l1l111l_opy_.shutdown()
            data = {
                bstack111lll_opy_ (u"ࠩࡩ࡭ࡳ࡯ࡳࡩࡧࡧࡣࡦࡺࠧὑ"): bstack1llllllll1_opy_()
            }
            if not bstack11111l11111_opy_ is None:
                data[bstack111lll_opy_ (u"ࠪࡪ࡮ࡴࡩࡴࡪࡨࡨࡤࡳࡥࡵࡣࡧࡥࡹࡧࠧὒ")] = [{
                    bstack111lll_opy_ (u"ࠫࡷ࡫ࡡࡴࡱࡱࠫὓ"): bstack111lll_opy_ (u"ࠬࡻࡳࡦࡴࡢ࡯࡮ࡲ࡬ࡦࡦࠪὔ"),
                    bstack111lll_opy_ (u"࠭ࡳࡪࡩࡱࡥࡱ࠭ὕ"): bstack11111l11111_opy_
                }]
            config = {
                bstack111lll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨὖ"): cls.default_headers()
            }
            bstack11ll1ll11l1_opy_ = bstack111lll_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡤࡸ࡭ࡱࡪࡳ࠰ࡽࢀ࠳ࡸࡺ࡯ࡱࠩὗ").format(os.environ[bstack111lll_opy_ (u"ࠤࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠢ὘")])
            bstack111111l1ll1_opy_ = cls.request_url(bstack11ll1ll11l1_opy_)
            response = bstack1l1ll1l111_opy_(bstack111lll_opy_ (u"ࠪࡔ࡚࡚ࠧὙ"), bstack111111l1ll1_opy_, data, config)
            if not response.ok:
                raise Exception(bstack111lll_opy_ (u"ࠦࡘࡺ࡯ࡱࠢࡵࡩࡶࡻࡥࡴࡶࠣࡲࡴࡺࠠࡰ࡭ࠥ὚"))
        except Exception as error:
            logger.error(bstack111lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺ࡯ࡱࠢࡥࡹ࡮ࡲࡤࠡࡴࡨࡵࡺ࡫ࡳࡵࠢࡷࡳ࡚ࠥࡥࡴࡶࡋࡹࡧࡀ࠺ࠡࠤὛ") + str(error))
            return {
                bstack111lll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭὜"): bstack111lll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭Ὕ"),
                bstack111lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ὞"): str(error)
            }
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    def bstack111111ll111_opy_(cls, response):
        bstack1111l1ll1_opy_ = response.json() if not isinstance(response, dict) else response
        bstack111111l11ll_opy_ = {}
        if bstack1111l1ll1_opy_.get(bstack111lll_opy_ (u"ࠩ࡭ࡻࡹ࠭Ὗ")) is None:
            os.environ[bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧὠ")] = bstack111lll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩὡ")
        else:
            os.environ[bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩὢ")] = bstack1111l1ll1_opy_.get(bstack111lll_opy_ (u"࠭ࡪࡸࡶࠪὣ"), bstack111lll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬὤ"))
        os.environ[bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ὥ")] = bstack1111l1ll1_opy_.get(bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫὦ"), bstack111lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨὧ"))
        logger.info(bstack111lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡪࡸࡦࠥࡹࡴࡢࡴࡷࡩࡩࠦࡷࡪࡶ࡫ࠤ࡮ࡪ࠺ࠡࠩὨ") + os.getenv(bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪὩ")));
        if bstack11l1ll111_opy_.bstack11111l11lll_opy_(cls.bs_config, cls.bstack1ll1l11l1l_opy_.get(bstack111lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧὪ"), bstack111lll_opy_ (u"ࠧࠨὫ"))) is True:
            bstack1111l11ll1l_opy_, build_hashed_id, bstack111111ll1l1_opy_ = cls.bstack11111l1ll11_opy_(bstack1111l1ll1_opy_)
            if bstack1111l11ll1l_opy_ != None and build_hashed_id != None:
                bstack111111l11ll_opy_[bstack111lll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨὬ")] = {
                    bstack111lll_opy_ (u"ࠩ࡭ࡻࡹࡥࡴࡰ࡭ࡨࡲࠬὭ"): bstack1111l11ll1l_opy_,
                    bstack111lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬὮ"): build_hashed_id,
                    bstack111lll_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡢࡷࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࡳࠨὯ"): bstack111111ll1l1_opy_
                }
            else:
                bstack111111l11ll_opy_[bstack111lll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬὰ")] = {}
        else:
            bstack111111l11ll_opy_[bstack111lll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ά")] = {}
        bstack111111ll1ll_opy_, build_hashed_id = cls.bstack111111lllll_opy_(bstack1111l1ll1_opy_)
        if bstack111111ll1ll_opy_ != None and build_hashed_id != None:
            bstack111111l11ll_opy_[bstack111lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧὲ")] = {
                bstack111lll_opy_ (u"ࠨࡣࡸࡸ࡭ࡥࡴࡰ࡭ࡨࡲࠬέ"): bstack111111ll1ll_opy_,
                bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫὴ"): build_hashed_id,
            }
        else:
            bstack111111l11ll_opy_[bstack111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪή")] = {}
        if bstack111111l11ll_opy_[bstack111lll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫὶ")].get(bstack111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧί")) != None or bstack111111l11ll_opy_[bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ὸ")].get(bstack111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩό")) != None:
            cls.bstack111111lll11_opy_(bstack1111l1ll1_opy_.get(bstack111lll_opy_ (u"ࠨ࡬ࡺࡸࠬὺ")), bstack1111l1ll1_opy_.get(bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫύ")))
        return bstack111111l11ll_opy_
    @classmethod
    def bstack11111l1ll11_opy_(cls, bstack1111l1ll1_opy_):
        if bstack1111l1ll1_opy_.get(bstack111lll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪὼ")) == None:
            cls.bstack111111ll11l_opy_()
            return [None, None, None]
        if bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫώ")][bstack111lll_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭὾")] != True:
            cls.bstack111111ll11l_opy_(bstack1111l1ll1_opy_[bstack111lll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭὿")])
            return [None, None, None]
        logger.debug(bstack111lll_opy_ (u"ࠧࡕࡧࡶࡸࠥࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫᾀ"))
        os.environ[bstack111lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡈࡕࡍࡑࡎࡈࡘࡊࡊࠧᾁ")] = bstack111lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᾂ")
        if bstack1111l1ll1_opy_.get(bstack111lll_opy_ (u"ࠪ࡮ࡼࡺࠧᾃ")):
            os.environ[bstack111lll_opy_ (u"ࠫࡈࡘࡅࡅࡇࡑࡘࡎࡇࡌࡔࡡࡉࡓࡗࡥࡃࡓࡃࡖࡌࡤࡘࡅࡑࡑࡕࡘࡎࡔࡇࠨᾄ")] = json.dumps({
                bstack111lll_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧᾅ"): bstack11lll111111_opy_(cls.bs_config),
                bstack111lll_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨᾆ"): bstack11llll111ll_opy_(cls.bs_config)
            })
        if bstack1111l1ll1_opy_.get(bstack111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᾇ")):
            os.environ[bstack111lll_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡈࡕࡊࡎࡇࡣࡍࡇࡓࡉࡇࡇࡣࡎࡊࠧᾈ")] = bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᾉ")]
        if bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪᾊ")].get(bstack111lll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᾋ"), {}).get(bstack111lll_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᾌ")):
            os.environ[bstack111lll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧᾍ")] = str(bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᾎ")][bstack111lll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᾏ")][bstack111lll_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᾐ")])
        else:
            os.environ[bstack111lll_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᾑ")] = bstack111lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᾒ")
        return [bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠬࡰࡷࡵࠩᾓ")], bstack1111l1ll1_opy_[bstack111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᾔ")], os.environ[bstack111lll_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᾕ")]]
    @classmethod
    def bstack111111lllll_opy_(cls, bstack1111l1ll1_opy_):
        if bstack1111l1ll1_opy_.get(bstack111lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᾖ")) == None:
            cls.bstack111111l1l1l_opy_()
            return [None, None]
        if bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᾗ")][bstack111lll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᾘ")] != True:
            cls.bstack111111l1l1l_opy_(bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᾙ")])
            return [None, None]
        if bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᾚ")].get(bstack111lll_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᾛ")):
            logger.debug(bstack111lll_opy_ (u"ࠧࡕࡧࡶࡸࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡓࡶࡥࡦࡩࡸࡹࡦࡶ࡮ࠤࠫᾜ"))
            parsed = json.loads(os.getenv(bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᾝ"), bstack111lll_opy_ (u"ࠩࡾࢁࠬᾞ")))
            capabilities = bstack1lll1l1l_opy_.bstack11111l111l1_opy_(bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᾟ")][bstack111lll_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᾠ")][bstack111lll_opy_ (u"ࠬࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᾡ")], bstack111lll_opy_ (u"࠭࡮ࡢ࡯ࡨࠫᾢ"), bstack111lll_opy_ (u"ࠧࡷࡣ࡯ࡹࡪ࠭ᾣ"))
            bstack111111ll1ll_opy_ = capabilities[bstack111lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭ᾤ")]
            os.environ[bstack111lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᾥ")] = bstack111111ll1ll_opy_
            if bstack111lll_opy_ (u"ࠥࡥࡺࡺ࡯࡮ࡣࡷࡩࠧᾦ") in bstack1111l1ll1_opy_ and bstack1111l1ll1_opy_.get(bstack111lll_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥᾧ")) is None:
                parsed[bstack111lll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᾨ")] = capabilities[bstack111lll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᾩ")]
            os.environ[bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᾪ")] = json.dumps(parsed)
            scripts = bstack1lll1l1l_opy_.bstack11111l111l1_opy_(bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᾫ")][bstack111lll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᾬ")][bstack111lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᾭ")], bstack111lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᾮ"), bstack111lll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࠭ᾯ"))
            bstack11ll1l1ll_opy_.bstack1ll1l11l1_opy_(scripts)
            commands = bstack1111l1ll1_opy_[bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᾰ")][bstack111lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨᾱ")][bstack111lll_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠩᾲ")].get(bstack111lll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᾳ"))
            bstack11ll1l1ll_opy_.bstack11lll1lll11_opy_(commands)
            bstack11lll1111ll_opy_ = capabilities.get(bstack111lll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᾴ"))
            bstack11ll1l1ll_opy_.bstack11ll1ll1ll1_opy_(bstack11lll1111ll_opy_)
            bstack11ll1l1ll_opy_.store()
        return [bstack111111ll1ll_opy_, bstack1111l1ll1_opy_[bstack111lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭᾵")]]
    @classmethod
    def bstack111111ll11l_opy_(cls, response=None):
        os.environ[bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᾶ")] = bstack111lll_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᾷ")
        os.environ[bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᾸ")] = bstack111lll_opy_ (u"ࠨࡰࡸࡰࡱ࠭Ᾱ")
        os.environ[bstack111lll_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡂࡖࡋࡏࡈࡤࡉࡏࡎࡒࡏࡉ࡙ࡋࡄࠨᾺ")] = bstack111lll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩΆ")
        os.environ[bstack111lll_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡔࡖࡓࡠࡄࡘࡍࡑࡊ࡟ࡉࡃࡖࡌࡊࡊ࡟ࡊࡆࠪᾼ")] = bstack111lll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ᾽")
        os.environ[bstack111lll_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡅࡑࡒࡏࡘࡡࡖࡇࡗࡋࡅࡏࡕࡋࡓ࡙࡙ࠧι")] = bstack111lll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧ᾿")
        cls.bstack111111l1lll_opy_(response, bstack111lll_opy_ (u"ࠣࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠣ῀"))
        return [None, None, None]
    @classmethod
    def bstack111111l1l1l_opy_(cls, response=None):
        os.environ[bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ῁")] = bstack111lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨῂ")
        os.environ[bstack111lll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩῃ")] = bstack111lll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪῄ")
        os.environ[bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ῅")] = bstack111lll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬῆ")
        cls.bstack111111l1lll_opy_(response, bstack111lll_opy_ (u"ࠣࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠣῇ"))
        return [None, None, None]
    @classmethod
    def bstack111111lll11_opy_(cls, jwt, build_hashed_id):
        os.environ[bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭Ὲ")] = jwt
        os.environ[bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨΈ")] = build_hashed_id
    @classmethod
    def bstack111111l1lll_opy_(cls, response=None, product=bstack111lll_opy_ (u"ࠦࠧῊ")):
        if response == None or response.get(bstack111lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬΉ")) == None:
            logger.error(product + bstack111lll_opy_ (u"ࠨࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠣῌ"))
            return
        for error in response[bstack111lll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧ῍")]:
            bstack11l11ll11ll_opy_ = error[bstack111lll_opy_ (u"ࠨ࡭ࡨࡽࠬ῎")]
            error_message = error[bstack111lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ῏")]
            if error_message:
                if bstack11l11ll11ll_opy_ == bstack111lll_opy_ (u"ࠥࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠤῐ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack111lll_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࠧῑ") + product + bstack111lll_opy_ (u"ࠧࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥῒ"))
    @classmethod
    def bstack11111l1l1ll_opy_(cls):
        if cls.bstack1111l1l111l_opy_ is not None:
            return
        cls.bstack1111l1l111l_opy_ = bstack1111l1l11ll_opy_(cls.bstack11111l1111l_opy_)
        cls.bstack1111l1l111l_opy_.start()
    @classmethod
    def bstack111ll11l11_opy_(cls):
        if cls.bstack1111l1l111l_opy_ is None:
            return
        cls.bstack1111l1l111l_opy_.shutdown()
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    def bstack11111l1111l_opy_(cls, bstack111l11ll11_opy_, event_url=bstack111lll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬΐ")):
        config = {
            bstack111lll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ῔"): cls.default_headers()
        }
        logger.debug(bstack111lll_opy_ (u"ࠣࡲࡲࡷࡹࡥࡤࡢࡶࡤ࠾࡙ࠥࡥ࡯ࡦ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤࡹࡵࠠࡵࡧࡶࡸ࡭ࡻࡢࠡࡨࡲࡶࠥ࡫ࡶࡦࡰࡷࡷࠥࢁࡽࠣ῕").format(bstack111lll_opy_ (u"ࠩ࠯ࠤࠬῖ").join([event[bstack111lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧῗ")] for event in bstack111l11ll11_opy_])))
        response = bstack1l1ll1l111_opy_(bstack111lll_opy_ (u"ࠫࡕࡕࡓࡕࠩῘ"), cls.request_url(event_url), bstack111l11ll11_opy_, config)
        bstack11lll11ll1l_opy_ = response.json()
    @classmethod
    def bstack11111111l_opy_(cls, bstack111l11ll11_opy_, event_url=bstack111lll_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠵࠴ࡨࡡࡵࡥ࡫ࠫῙ")):
        logger.debug(bstack111lll_opy_ (u"ࠨࡳࡦࡰࡧࡣࡩࡧࡴࡢ࠼ࠣࡅࡹࡺࡥ࡮ࡲࡷ࡭ࡳ࡭ࠠࡵࡱࠣࡥࡩࡪࠠࡥࡣࡷࡥࠥࡺ࡯ࠡࡤࡤࡸࡨ࡮ࠠࡸ࡫ࡷ࡬ࠥ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦ࠼ࠣࡿࢂࠨῚ").format(bstack111l11ll11_opy_[bstack111lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫΊ")]))
        if not bstack1lll1l1l_opy_.bstack11111l11ll1_opy_(bstack111l11ll11_opy_[bstack111lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬ῜")]):
            logger.debug(bstack111lll_opy_ (u"ࠤࡶࡩࡳࡪ࡟ࡥࡣࡷࡥ࠿ࠦࡎࡰࡶࠣࡥࡩࡪࡩ࡯ࡩࠣࡨࡦࡺࡡࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢ῝").format(bstack111l11ll11_opy_[bstack111lll_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧ῞")]))
            return
        bstack11ll1ll1ll_opy_ = bstack1lll1l1l_opy_.bstack11111l1l11l_opy_(bstack111l11ll11_opy_[bstack111lll_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨ῟")], bstack111l11ll11_opy_.get(bstack111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧῠ")))
        if bstack11ll1ll1ll_opy_ != None:
            if bstack111l11ll11_opy_.get(bstack111lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࠨῡ")) != None:
                bstack111l11ll11_opy_[bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࠩῢ")][bstack111lll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭ΰ")] = bstack11ll1ll1ll_opy_
            else:
                bstack111l11ll11_opy_[bstack111lll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧῤ")] = bstack11ll1ll1ll_opy_
        if event_url == bstack111lll_opy_ (u"ࠪࡥࡵ࡯࠯ࡷ࠳࠲ࡦࡦࡺࡣࡩࠩῥ"):
            cls.bstack11111l1l1ll_opy_()
            logger.debug(bstack111lll_opy_ (u"ࠦࡸ࡫࡮ࡥࡡࡧࡥࡹࡧ࠺ࠡࡃࡧࡨ࡮ࡴࡧࠡࡦࡤࡸࡦࠦࡴࡰࠢࡥࡥࡹࡩࡨࠡࡹ࡬ࡸ࡭ࠦࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧ࠽ࠤࢀࢃࠢῦ").format(bstack111l11ll11_opy_[bstack111lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩῧ")]))
            cls.bstack1111l1l111l_opy_.add(bstack111l11ll11_opy_)
        elif event_url == bstack111lll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫῨ"):
            cls.bstack11111l1111l_opy_([bstack111l11ll11_opy_], event_url)
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    def bstack11l1111ll_opy_(cls, logs):
        bstack111111l11l1_opy_ = []
        for log in logs:
            bstack11111l1l111_opy_ = {
                bstack111lll_opy_ (u"ࠧ࡬࡫ࡱࡨࠬῩ"): bstack111lll_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡌࡐࡉࠪῪ"),
                bstack111lll_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨΎ"): log[bstack111lll_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩῬ")],
                bstack111lll_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ῭"): log[bstack111lll_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ΅")],
                bstack111lll_opy_ (u"࠭ࡨࡵࡶࡳࡣࡷ࡫ࡳࡱࡱࡱࡷࡪ࠭`"): {},
                bstack111lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ῰"): log[bstack111lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ῱")],
            }
            if bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩῲ") in log:
                bstack11111l1l111_opy_[bstack111lll_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪῳ")] = log[bstack111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫῴ")]
            elif bstack111lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ῵") in log:
                bstack11111l1l111_opy_[bstack111lll_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ῶ")] = log[bstack111lll_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧῷ")]
            bstack111111l11l1_opy_.append(bstack11111l1l111_opy_)
        cls.bstack11111111l_opy_({
            bstack111lll_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬῸ"): bstack111lll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭Ό"),
            bstack111lll_opy_ (u"ࠪࡰࡴ࡭ࡳࠨῺ"): bstack111111l11l1_opy_
        })
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    def bstack11111l111ll_opy_(cls, steps):
        bstack111111lll1l_opy_ = []
        for step in steps:
            bstack11111l1l1l1_opy_ = {
                bstack111lll_opy_ (u"ࠫࡰ࡯࡮ࡥࠩΏ"): bstack111lll_opy_ (u"࡚ࠬࡅࡔࡖࡢࡗ࡙ࡋࡐࠨῼ"),
                bstack111lll_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ´"): step[bstack111lll_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭῾")],
                bstack111lll_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ῿"): step[bstack111lll_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ ")],
                bstack111lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ "): step[bstack111lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ ")],
                bstack111lll_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧ "): step[bstack111lll_opy_ (u"࠭ࡤࡶࡴࡤࡸ࡮ࡵ࡮ࠨ ")]
            }
            if bstack111lll_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧ ") in step:
                bstack11111l1l1l1_opy_[bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨ ")] = step[bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩ ")]
            elif bstack111lll_opy_ (u"ࠪ࡬ࡴࡵ࡫ࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪ ") in step:
                bstack11111l1l1l1_opy_[bstack111lll_opy_ (u"ࠫ࡭ࡵ࡯࡬ࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ ")] = step[bstack111lll_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ ")]
            bstack111111lll1l_opy_.append(bstack11111l1l1l1_opy_)
        cls.bstack11111111l_opy_({
            bstack111lll_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡺࡹࡱࡧࠪ​"): bstack111lll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ‌"),
            bstack111lll_opy_ (u"ࠨ࡮ࡲ࡫ࡸ࠭‍"): bstack111111lll1l_opy_
        })
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    @measure(event_name=EVENTS.bstack11l1111ll1_opy_, stage=STAGE.bstack111ll11l1_opy_)
    def bstack1l111lll_opy_(cls, screenshot):
        cls.bstack11111111l_opy_({
            bstack111lll_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭‎"): bstack111lll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ‏"),
            bstack111lll_opy_ (u"ࠫࡱࡵࡧࡴࠩ‐"): [{
                bstack111lll_opy_ (u"ࠬࡱࡩ࡯ࡦࠪ‑"): bstack111lll_opy_ (u"࠭ࡔࡆࡕࡗࡣࡘࡉࡒࡆࡇࡑࡗࡍࡕࡔࠨ‒"),
                bstack111lll_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪ–"): datetime.datetime.utcnow().isoformat() + bstack111lll_opy_ (u"ࠨ࡜ࠪ—"),
                bstack111lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ―"): screenshot[bstack111lll_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩ‖")],
                bstack111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫ‗"): screenshot[bstack111lll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ‘")]
            }]
        }, event_url=bstack111lll_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࡶࠫ’"))
    @classmethod
    @bstack111l1ll1l1_opy_(class_method=True)
    def bstack111111lll_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11111111l_opy_({
            bstack111lll_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ‚"): bstack111lll_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬ‛"),
            bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࠫ“"): {
                bstack111lll_opy_ (u"ࠥࡹࡺ࡯ࡤࠣ”"): cls.current_test_uuid(),
                bstack111lll_opy_ (u"ࠦ࡮ࡴࡴࡦࡩࡵࡥࡹ࡯࡯࡯ࡵࠥ„"): cls.bstack111lll1lll_opy_(driver)
            }
        })
    @classmethod
    def bstack111lllllll_opy_(cls, event: str, bstack111l11ll11_opy_: bstack111l1l1111_opy_):
        bstack111l11llll_opy_ = {
            bstack111lll_opy_ (u"ࠬ࡫ࡶࡦࡰࡷࡣࡹࡿࡰࡦࠩ‟"): event,
            bstack111l11ll11_opy_.bstack1111llll11_opy_(): bstack111l11ll11_opy_.bstack111l111l11_opy_(event)
        }
        cls.bstack11111111l_opy_(bstack111l11llll_opy_)
        result = getattr(bstack111l11ll11_opy_, bstack111lll_opy_ (u"࠭ࡲࡦࡵࡸࡰࡹ࠭†"), None)
        if event == bstack111lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ‡"):
            threading.current_thread().bstackTestMeta = {bstack111lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ•"): bstack111lll_opy_ (u"ࠩࡳࡩࡳࡪࡩ࡯ࡩࠪ‣")}
        elif event == bstack111lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ․"):
            threading.current_thread().bstackTestMeta = {bstack111lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ‥"): getattr(result, bstack111lll_opy_ (u"ࠬࡸࡥࡴࡷ࡯ࡸࠬ…"), bstack111lll_opy_ (u"࠭ࠧ‧"))}
    @classmethod
    def on(cls):
        if (os.environ.get(bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ "), None) is None or os.environ[bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ ")] == bstack111lll_opy_ (u"ࠤࡱࡹࡱࡲࠢ‪")) and (os.environ.get(bstack111lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ‫"), None) is None or os.environ[bstack111lll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ‬")] == bstack111lll_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ‭")):
            return False
        return True
    @staticmethod
    def bstack11111l11l1l_opy_(func):
        def wrap(*args, **kwargs):
            if bstack11111ll1l_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack111lll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ‮"): bstack111lll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ "),
            bstack111lll_opy_ (u"ࠨ࡚࠰ࡆࡘ࡚ࡁࡄࡍ࠰ࡘࡊ࡙ࡔࡐࡒࡖࠫ‰"): bstack111lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ‱")
        }
        if os.environ.get(bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ′"), None):
            headers[bstack111lll_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫ″")] = bstack111lll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥࢁࡽࠨ‴").format(os.environ[bstack111lll_opy_ (u"ࠨࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠥ‵")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack111lll_opy_ (u"ࠧࡼࡿ࠲ࡿࢂ࠭‶").format(bstack111111l1l11_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack111lll_opy_ (u"ࠨࡥࡸࡶࡷ࡫࡮ࡵࡡࡷࡩࡸࡺ࡟ࡶࡷ࡬ࡨࠬ‷"), None)
    @staticmethod
    def bstack111lll1lll_opy_(driver):
        return {
            bstack11l1l1ll1ll_opy_(): bstack11l1l11lll1_opy_(driver)
        }
    @staticmethod
    def bstack111111llll1_opy_(exception_info, report):
        return [{bstack111lll_opy_ (u"ࠩࡥࡥࡨࡱࡴࡳࡣࡦࡩࠬ‸"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11111lllll_opy_(typename):
        if bstack111lll_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ‹") in typename:
            return bstack111lll_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ›")
        return bstack111lll_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ※")