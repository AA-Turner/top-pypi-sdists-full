# coding: UTF-8
import sys
bstack1l11111_opy_ = sys.version_info [0] == 2
bstack1ll_opy_ = 2048
bstack1l1lll1_opy_ = 7
def bstack1ll1ll_opy_ (bstack11l1l1_opy_):
    global bstack1ll1l1_opy_
    bstack1ll1111_opy_ = ord (bstack11l1l1_opy_ [-1])
    bstack1l1l1l_opy_ = bstack11l1l1_opy_ [:-1]
    bstack11l11_opy_ = bstack1ll1111_opy_ % len (bstack1l1l1l_opy_)
    bstack1l111_opy_ = bstack1l1l1l_opy_ [:bstack11l11_opy_] + bstack1l1l1l_opy_ [bstack11l11_opy_:]
    if bstack1l11111_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1ll_opy_ - (bstack11ll1l_opy_ + bstack1ll1111_opy_) % bstack1l1lll1_opy_) for bstack11ll1l_opy_, char in enumerate (bstack1l111_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11ll1llll11_opy_, bstack111l1l1l1_opy_, get_host_info, bstack11l1111lll1_opy_, \
 bstack1ll11lll1_opy_, bstack11l1llllll_opy_, error_handler, bstack11l1l11l111_opy_, bstack1l111ll1_opy_
import bstack_utils.accessibility as bstack1ll1ll1lll_opy_
from bstack_utils.bstack11llllll11_opy_ import bstack1111lll1_opy_
from bstack_utils.bstack111ll1l11l_opy_ import bstack11llllll1_opy_
from bstack_utils.percy import bstack11ll1l1ll_opy_
from bstack_utils.config import Config
bstack1llll11l_opy_ = Config.bstack1l11llllll_opy_()
logger = logging.getLogger(__name__)
percy = bstack11ll1l1ll_opy_()
@error_handler(class_method=False)
def bstack1llll1lll111_opy_(bs_config, bstack1llll1lll_opy_):
  try:
    data = {
        bstack1ll1ll_opy_ (u"ࠩࡩࡳࡷࡳࡡࡵࠩ↖"): bstack1ll1ll_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨ↗"),
        bstack1ll1ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡤࡴࡡ࡮ࡧࠪ↘"): bs_config.get(bstack1ll1ll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ↙"), bstack1ll1ll_opy_ (u"࠭ࠧ↚")),
        bstack1ll1ll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ↛"): bs_config.get(bstack1ll1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ↜"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1ll1ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ↝"): bs_config.get(bstack1ll1ll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ↞")),
        bstack1ll1ll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ↟"): bs_config.get(bstack1ll1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ↠"), bstack1ll1ll_opy_ (u"࠭ࠧ↡")),
        bstack1ll1ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ↢"): bstack1l111ll1_opy_(),
        bstack1ll1ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭↣"): bstack11l1111lll1_opy_(bs_config),
        bstack1ll1ll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠬ↤"): get_host_info(),
        bstack1ll1ll_opy_ (u"ࠪࡧ࡮ࡥࡩ࡯ࡨࡲࠫ↥"): bstack111l1l1l1_opy_(),
        bstack1ll1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡶࡺࡴ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ↦"): os.environ.get(bstack1ll1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ↧")),
        bstack1ll1ll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࡸࡥࡳࡷࡱࠫ↨"): os.environ.get(bstack1ll1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬ↩"), False),
        bstack1ll1ll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡡࡦࡳࡳࡺࡲࡰ࡮ࠪ↪"): bstack11ll1llll11_opy_(),
        bstack1ll1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ↫"): bstack1llll1l11l1l_opy_(bs_config),
        bstack1ll1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡤࡦࡶࡤ࡭ࡱࡹࠧ↬"): bstack1llll1l111ll_opy_(bstack1llll1lll_opy_),
        bstack1ll1ll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ↭"): bstack1llll1l1l111_opy_(bs_config, bstack1llll1lll_opy_.get(bstack1ll1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭↮"), bstack1ll1ll_opy_ (u"࠭ࠧ↯"))),
        bstack1ll1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ↰"): bstack1ll11lll1_opy_(bs_config),
        bstack1ll1ll_opy_ (u"ࠨࡶࡨࡷࡹࡥ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠭↱"): bstack1llll1l11ll1_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1ll1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡢࡻ࡯ࡳࡦࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥ↲").format(str(error)))
    return None
def bstack1llll1l111ll_opy_(framework):
  return {
    bstack1ll1ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪ↳"): framework.get(bstack1ll1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬ↴"), bstack1ll1ll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ↵")),
    bstack1ll1ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ↶"): framework.get(bstack1ll1ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ↷")),
    bstack1ll1ll_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ↸"): framework.get(bstack1ll1ll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ↹")),
    bstack1ll1ll_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬ↺"): bstack1ll1ll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ↻"),
    bstack1ll1ll_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ↼"): framework.get(bstack1ll1ll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭↽"))
  }
def bstack1llll1l11ll1_opy_(bs_config):
  bstack1ll1ll_opy_ (u"ࠢࠣࠤࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡶࡸࡦࡸࡴ࠯ࠌࠣࠤࠧࠨࠢ↾")
  if not bs_config:
    return {}
  bstack111l11111ll_opy_ = bstack1111lll1_opy_(bs_config).bstack1111lllll1l_opy_(bs_config)
  return bstack111l11111ll_opy_
def bstack111l1ll1_opy_(bs_config, framework):
  bstack1lll11l1l1_opy_ = False
  bstack1llll111ll_opy_ = False
  bstack1llll1l1ll11_opy_ = False
  if bstack1ll1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ↿") in bs_config:
    bstack1llll1l1ll11_opy_ = True
  elif bstack1ll1ll_opy_ (u"ࠩࡤࡴࡵ࠭⇀") in bs_config:
    bstack1lll11l1l1_opy_ = True
  else:
    bstack1llll111ll_opy_ = True
  bstack11l1111l1_opy_ = {
    bstack1ll1ll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⇁"): bstack11llllll1_opy_.bstack1llll1l1lll1_opy_(bs_config, framework),
    bstack1ll1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⇂"): bstack1ll1ll1lll_opy_.bstack1lllllll11_opy_(bs_config),
    bstack1ll1ll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⇃"): bs_config.get(bstack1ll1ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⇄"), False),
    bstack1ll1ll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ⇅"): bstack1llll111ll_opy_,
    bstack1ll1ll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⇆"): bstack1lll11l1l1_opy_,
    bstack1ll1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭⇇"): bstack1llll1l1ll11_opy_
  }
  return bstack11l1111l1_opy_
@error_handler(class_method=False)
def bstack1llll1l11l1l_opy_(bs_config):
  try:
    bstack1llll1l11l11_opy_ = json.loads(os.getenv(bstack1ll1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ⇈"), bstack1ll1ll_opy_ (u"ࠫࢀࢃࠧ⇉")))
    bstack1llll1l11l11_opy_ = bstack1llll1l1l11l_opy_(bs_config, bstack1llll1l11l11_opy_)
    return {
        bstack1ll1ll_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧ⇊"): bstack1llll1l11l11_opy_
    }
  except Exception as error:
    logger.error(bstack1ll1ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ⇋").format(str(error)))
    return {}
def bstack1llll1l1l11l_opy_(bs_config, bstack1llll1l11l11_opy_):
  if ((bstack1ll1ll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⇌") in bs_config or not bstack1ll11lll1_opy_(bs_config)) and bstack1ll1ll1lll_opy_.bstack1lllllll11_opy_(bs_config)):
    bstack1llll1l11l11_opy_[bstack1ll1ll_opy_ (u"ࠣ࡫ࡱࡧࡱࡻࡤࡦࡇࡱࡧࡴࡪࡥࡥࡇࡻࡸࡪࡴࡳࡪࡱࡱࠦ⇍")] = True
  return bstack1llll1l11l11_opy_
def bstack1lllll11l111_opy_(array, bstack1llll1l1llll_opy_, bstack1llll1l1l1l1_opy_):
  result = {}
  for o in array:
    key = o[bstack1llll1l1llll_opy_]
    result[key] = o[bstack1llll1l1l1l1_opy_]
  return result
def bstack1lllll1111ll_opy_(bstack1l1ll1llll_opy_=bstack1ll1ll_opy_ (u"ࠩࠪ⇎")):
  bstack1llll1l11lll_opy_ = bstack1ll1ll1lll_opy_.on()
  bstack1llll1l1ll1l_opy_ = bstack11llllll1_opy_.on()
  bstack1llll1l111l1_opy_ = percy.bstack11l111ll_opy_()
  if bstack1llll1l111l1_opy_ and not bstack1llll1l1ll1l_opy_ and not bstack1llll1l11lll_opy_:
    return bstack1l1ll1llll_opy_ not in [bstack1ll1ll_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ⇏"), bstack1ll1ll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⇐")]
  elif bstack1llll1l11lll_opy_ and not bstack1llll1l1ll1l_opy_:
    return bstack1l1ll1llll_opy_ not in [bstack1ll1ll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⇑"), bstack1ll1ll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⇒"), bstack1ll1ll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⇓")]
  return bstack1llll1l11lll_opy_ or bstack1llll1l1ll1l_opy_ or bstack1llll1l111l1_opy_
@error_handler(class_method=False)
def bstack1lllll111l1l_opy_(bstack1l1ll1llll_opy_, test=None):
  bstack1llll1l1l1ll_opy_ = bstack1ll1ll1lll_opy_.on()
  if not bstack1llll1l1l1ll_opy_ or bstack1l1ll1llll_opy_ not in [bstack1ll1ll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⇔")] or test == None:
    return None
  return {
    bstack1ll1ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⇕"): bstack1llll1l1l1ll_opy_ and bstack11l1llllll_opy_(threading.current_thread(), bstack1ll1ll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⇖"), None) == True and bstack1ll1ll1lll_opy_.bstack1l1111llll_opy_(test[bstack1ll1ll_opy_ (u"ࠫࡹࡧࡧࡴࠩ⇗")])
  }
def bstack1llll1l1l111_opy_(bs_config, framework):
  bstack1lll11l1l1_opy_ = False
  bstack1llll111ll_opy_ = False
  bstack1llll1l1ll11_opy_ = False
  if bstack1ll1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⇘") in bs_config:
    bstack1llll1l1ll11_opy_ = True
  elif bstack1ll1ll_opy_ (u"࠭ࡡࡱࡲࠪ⇙") in bs_config:
    bstack1lll11l1l1_opy_ = True
  else:
    bstack1llll111ll_opy_ = True
  bstack11l1111l1_opy_ = {
    bstack1ll1ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⇚"): bstack11llllll1_opy_.bstack1llll1l1lll1_opy_(bs_config, framework),
    bstack1ll1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⇛"): bstack1ll1ll1lll_opy_.bstack1ll1llll1l_opy_(bs_config),
    bstack1ll1ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⇜"): bs_config.get(bstack1ll1ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⇝"), False),
    bstack1ll1ll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⇞"): bstack1llll111ll_opy_,
    bstack1ll1ll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⇟"): bstack1lll11l1l1_opy_,
    bstack1ll1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ⇠"): bstack1llll1l1ll11_opy_
  }
  return bstack11l1111l1_opy_