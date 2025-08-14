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
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11ll1ll11l1_opy_, bstack1llll1llll_opy_, get_host_info, bstack11l11llllll_opy_, \
 bstack1l1l11llll_opy_, bstack1l111l1l_opy_, error_handler, bstack111ll1lll1l_opy_, bstack11lllll1_opy_
import bstack_utils.accessibility as bstack1lll11l1ll_opy_
from bstack_utils.bstack11l1l111l1_opy_ import bstack1l1l1llll1_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1l1ll1l11l_opy_
from bstack_utils.percy import bstack1lllllll1_opy_
from bstack_utils.config import Config
bstack1l1l1111l1_opy_ = Config.bstack11l1lllll1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1lllllll1_opy_()
@error_handler(class_method=False)
def bstack1lllll111111_opy_(bs_config, bstack11ll11111_opy_):
  try:
    data = {
        bstack1l1l1ll_opy_ (u"ࠩࡩࡳࡷࡳࡡࡵࠩ↤"): bstack1l1l1ll_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨ↥"),
        bstack1l1l1ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡤࡴࡡ࡮ࡧࠪ↦"): bs_config.get(bstack1l1l1ll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ↧"), bstack1l1l1ll_opy_ (u"࠭ࠧ↨")),
        bstack1l1l1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ↩"): bs_config.get(bstack1l1l1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ↪"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1l1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ↫"): bs_config.get(bstack1l1l1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ↬")),
        bstack1l1l1ll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ↭"): bs_config.get(bstack1l1l1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ↮"), bstack1l1l1ll_opy_ (u"࠭ࠧ↯")),
        bstack1l1l1ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ↰"): bstack11lllll1_opy_(),
        bstack1l1l1ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭↱"): bstack11l11llllll_opy_(bs_config),
        bstack1l1l1ll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠬ↲"): get_host_info(),
        bstack1l1l1ll_opy_ (u"ࠪࡧ࡮ࡥࡩ࡯ࡨࡲࠫ↳"): bstack1llll1llll_opy_(),
        bstack1l1l1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡶࡺࡴ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ↴"): os.environ.get(bstack1l1l1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ↵")),
        bstack1l1l1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࡸࡥࡳࡷࡱࠫ↶"): os.environ.get(bstack1l1l1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬ↷"), False),
        bstack1l1l1ll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡡࡦࡳࡳࡺࡲࡰ࡮ࠪ↸"): bstack11ll1ll11l1_opy_(),
        bstack1l1l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ↹"): bstack1llll1l1l11l_opy_(bs_config),
        bstack1l1l1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡤࡦࡶࡤ࡭ࡱࡹࠧ↺"): bstack1llll1l1l111_opy_(bstack11ll11111_opy_),
        bstack1l1l1ll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ↻"): bstack1llll1l11lll_opy_(bs_config, bstack11ll11111_opy_.get(bstack1l1l1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭↼"), bstack1l1l1ll_opy_ (u"࠭ࠧ↽"))),
        bstack1l1l1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ↾"): bstack1l1l11llll_opy_(bs_config),
        bstack1l1l1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠭↿"): bstack1llll1l11l11_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1l1l1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡢࡻ࡯ࡳࡦࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥ⇀").format(str(error)))
    return None
def bstack1llll1l1l111_opy_(framework):
  return {
    bstack1l1l1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪ⇁"): framework.get(bstack1l1l1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬ⇂"), bstack1l1l1ll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ⇃")),
    bstack1l1l1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ⇄"): framework.get(bstack1l1l1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⇅")),
    bstack1l1l1ll_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ⇆"): framework.get(bstack1l1l1ll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⇇")),
    bstack1l1l1ll_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬ⇈"): bstack1l1l1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⇉"),
    bstack1l1l1ll_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⇊"): framework.get(bstack1l1l1ll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⇋"))
  }
def bstack1llll1l11l11_opy_(bs_config):
  bstack1l1l1ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡶࡸࡦࡸࡴ࠯ࠌࠣࠤࠧࠨࠢ⇌")
  if not bs_config:
    return {}
  bstack1111lll1ll1_opy_ = bstack1l1l1llll1_opy_(bs_config).bstack111l111l111_opy_(bs_config)
  return bstack1111lll1ll1_opy_
def bstack1l1l111ll1_opy_(bs_config, framework):
  bstack11l1llll11_opy_ = False
  bstack1ll1l1l1l_opy_ = False
  bstack1llll1l1ll1l_opy_ = False
  if bstack1l1l1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⇍") in bs_config:
    bstack1llll1l1ll1l_opy_ = True
  elif bstack1l1l1ll_opy_ (u"ࠩࡤࡴࡵ࠭⇎") in bs_config:
    bstack11l1llll11_opy_ = True
  else:
    bstack1ll1l1l1l_opy_ = True
  bstack1lll1l1lll_opy_ = {
    bstack1l1l1ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⇏"): bstack1l1ll1l11l_opy_.bstack1llll1l11111_opy_(bs_config, framework),
    bstack1l1l1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⇐"): bstack1lll11l1ll_opy_.bstack11l11ll11_opy_(bs_config),
    bstack1l1l1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⇑"): bs_config.get(bstack1l1l1ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⇒"), False),
    bstack1l1l1ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ⇓"): bstack1ll1l1l1l_opy_,
    bstack1l1l1ll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⇔"): bstack11l1llll11_opy_,
    bstack1l1l1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭⇕"): bstack1llll1l1ll1l_opy_
  }
  return bstack1lll1l1lll_opy_
@error_handler(class_method=False)
def bstack1llll1l1l11l_opy_(bs_config):
  try:
    bstack1llll1l1l1ll_opy_ = json.loads(os.getenv(bstack1l1l1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ⇖"), bstack1l1l1ll_opy_ (u"ࠫࢀࢃࠧ⇗")))
    bstack1llll1l1l1ll_opy_ = bstack1llll1l11l1l_opy_(bs_config, bstack1llll1l1l1ll_opy_)
    return {
        bstack1l1l1ll_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧ⇘"): bstack1llll1l1l1ll_opy_
    }
  except Exception as error:
    logger.error(bstack1l1l1ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ⇙").format(str(error)))
    return {}
def bstack1llll1l11l1l_opy_(bs_config, bstack1llll1l1l1ll_opy_):
  if ((bstack1l1l1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⇚") in bs_config or not bstack1l1l11llll_opy_(bs_config)) and bstack1lll11l1ll_opy_.bstack11l11ll11_opy_(bs_config)):
    bstack1llll1l1l1ll_opy_[bstack1l1l1ll_opy_ (u"ࠣ࡫ࡱࡧࡱࡻࡤࡦࡇࡱࡧࡴࡪࡥࡥࡇࡻࡸࡪࡴࡳࡪࡱࡱࠦ⇛")] = True
  return bstack1llll1l1l1ll_opy_
def bstack1llll1lll111_opy_(array, bstack1llll1l111l1_opy_, bstack1llll1l11ll1_opy_):
  result = {}
  for o in array:
    key = o[bstack1llll1l111l1_opy_]
    result[key] = o[bstack1llll1l11ll1_opy_]
  return result
def bstack1llll1ll1ll1_opy_(bstack1l1l1ll1_opy_=bstack1l1l1ll_opy_ (u"ࠩࠪ⇜")):
  bstack1llll1l1l1l1_opy_ = bstack1lll11l1ll_opy_.on()
  bstack1llll1l1ll11_opy_ = bstack1l1ll1l11l_opy_.on()
  bstack1llll1l1111l_opy_ = percy.bstack111l1111l_opy_()
  if bstack1llll1l1111l_opy_ and not bstack1llll1l1ll11_opy_ and not bstack1llll1l1l1l1_opy_:
    return bstack1l1l1ll1_opy_ not in [bstack1l1l1ll_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ⇝"), bstack1l1l1ll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⇞")]
  elif bstack1llll1l1l1l1_opy_ and not bstack1llll1l1ll11_opy_:
    return bstack1l1l1ll1_opy_ not in [bstack1l1l1ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⇟"), bstack1l1l1ll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⇠"), bstack1l1l1ll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⇡")]
  return bstack1llll1l1l1l1_opy_ or bstack1llll1l1ll11_opy_ or bstack1llll1l1111l_opy_
@error_handler(class_method=False)
def bstack1llll1ll11ll_opy_(bstack1l1l1ll1_opy_, test=None):
  bstack1llll1l111ll_opy_ = bstack1lll11l1ll_opy_.on()
  if not bstack1llll1l111ll_opy_ or bstack1l1l1ll1_opy_ not in [bstack1l1l1ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⇢")] or test == None:
    return None
  return {
    bstack1l1l1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⇣"): bstack1llll1l111ll_opy_ and bstack1l111l1l_opy_(threading.current_thread(), bstack1l1l1ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⇤"), None) == True and bstack1lll11l1ll_opy_.bstack111l1lll1_opy_(test[bstack1l1l1ll_opy_ (u"ࠫࡹࡧࡧࡴࠩ⇥")])
  }
def bstack1llll1l11lll_opy_(bs_config, framework):
  bstack11l1llll11_opy_ = False
  bstack1ll1l1l1l_opy_ = False
  bstack1llll1l1ll1l_opy_ = False
  if bstack1l1l1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⇦") in bs_config:
    bstack1llll1l1ll1l_opy_ = True
  elif bstack1l1l1ll_opy_ (u"࠭ࡡࡱࡲࠪ⇧") in bs_config:
    bstack11l1llll11_opy_ = True
  else:
    bstack1ll1l1l1l_opy_ = True
  bstack1lll1l1lll_opy_ = {
    bstack1l1l1ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⇨"): bstack1l1ll1l11l_opy_.bstack1llll1l11111_opy_(bs_config, framework),
    bstack1l1l1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⇩"): bstack1lll11l1ll_opy_.bstack11l1111111_opy_(bs_config),
    bstack1l1l1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⇪"): bs_config.get(bstack1l1l1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⇫"), False),
    bstack1l1l1ll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⇬"): bstack1ll1l1l1l_opy_,
    bstack1l1l1ll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⇭"): bstack11l1llll11_opy_,
    bstack1l1l1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ⇮"): bstack1llll1l1ll1l_opy_
  }
  return bstack1lll1l1lll_opy_