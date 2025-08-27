# coding: UTF-8
import sys
bstack1ll1111_opy_ = sys.version_info [0] == 2
bstack1111l1l_opy_ = 2048
bstack1l111_opy_ = 7
def bstack1111lll_opy_ (bstack1llll11_opy_):
    global bstack1llll1_opy_
    bstack1l111l_opy_ = ord (bstack1llll11_opy_ [-1])
    bstack11111l_opy_ = bstack1llll11_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1l111l_opy_ % len (bstack11111l_opy_)
    bstack1l111l1_opy_ = bstack11111l_opy_ [:bstack1l11ll_opy_] + bstack11111l_opy_ [bstack1l11ll_opy_:]
    if bstack1ll1111_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111l1l_opy_ - (bstack1l11l_opy_ + bstack1l111l_opy_) % bstack1l111_opy_) for bstack1l11l_opy_, char in enumerate (bstack1l111l1_opy_)])
    return eval (bstack1_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11ll1ll1lll_opy_, bstack1l111ll11l_opy_, get_host_info, bstack111ll1llll1_opy_, \
 bstack11l1111l1l_opy_, bstack1l11l1l1ll_opy_, error_handler, bstack111ll1l1ll1_opy_, bstack11l11ll1l1_opy_
import bstack_utils.accessibility as bstack1llllll1l1_opy_
from bstack_utils.bstack111l111ll_opy_ import bstack1l11llll1_opy_
from bstack_utils.bstack111lll11l1_opy_ import bstack1ll11l1ll1_opy_
from bstack_utils.percy import bstack1llllllll_opy_
from bstack_utils.config import Config
bstack1ll111ll11_opy_ = Config.bstack1ll1lll1l1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1llllllll_opy_()
@error_handler(class_method=False)
def bstack1llll1l1lll1_opy_(bs_config, bstack1l111lll1l_opy_):
  try:
    data = {
        bstack1111lll_opy_ (u"ࠩࡩࡳࡷࡳࡡࡵࠩ↖"): bstack1111lll_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨ↗"),
        bstack1111lll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡤࡴࡡ࡮ࡧࠪ↘"): bs_config.get(bstack1111lll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ↙"), bstack1111lll_opy_ (u"࠭ࠧ↚")),
        bstack1111lll_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ↛"): bs_config.get(bstack1111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ↜"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ↝"): bs_config.get(bstack1111lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ↞")),
        bstack1111lll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ↟"): bs_config.get(bstack1111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ↠"), bstack1111lll_opy_ (u"࠭ࠧ↡")),
        bstack1111lll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ↢"): bstack11l11ll1l1_opy_(),
        bstack1111lll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭↣"): bstack111ll1llll1_opy_(bs_config),
        bstack1111lll_opy_ (u"ࠩ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠬ↤"): get_host_info(),
        bstack1111lll_opy_ (u"ࠪࡧ࡮ࡥࡩ࡯ࡨࡲࠫ↥"): bstack1l111ll11l_opy_(),
        bstack1111lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡶࡺࡴ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ↦"): os.environ.get(bstack1111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ↧")),
        bstack1111lll_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࡸࡥࡳࡷࡱࠫ↨"): os.environ.get(bstack1111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬ↩"), False),
        bstack1111lll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡡࡦࡳࡳࡺࡲࡰ࡮ࠪ↪"): bstack11ll1ll1lll_opy_(),
        bstack1111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ↫"): bstack1llll1l111l1_opy_(bs_config),
        bstack1111lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡤࡦࡶࡤ࡭ࡱࡹࠧ↬"): bstack1llll11l1ll1_opy_(bstack1l111lll1l_opy_),
        bstack1111lll_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ↭"): bstack1llll11ll1l1_opy_(bs_config, bstack1l111lll1l_opy_.get(bstack1111lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭↮"), bstack1111lll_opy_ (u"࠭ࠧ↯"))),
        bstack1111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ↰"): bstack11l1111l1l_opy_(bs_config),
        bstack1111lll_opy_ (u"ࠨࡶࡨࡷࡹࡥ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠭↱"): bstack1llll11llll1_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1111lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡢࡻ࡯ࡳࡦࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥ↲").format(str(error)))
    return None
def bstack1llll11l1ll1_opy_(framework):
  return {
    bstack1111lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪ↳"): framework.get(bstack1111lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬ↴"), bstack1111lll_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ↵")),
    bstack1111lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ↶"): framework.get(bstack1111lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ↷")),
    bstack1111lll_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ↸"): framework.get(bstack1111lll_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ↹")),
    bstack1111lll_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬ↺"): bstack1111lll_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ↻"),
    bstack1111lll_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ↼"): framework.get(bstack1111lll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭↽"))
  }
def bstack1llll11llll1_opy_(bs_config):
  bstack1111lll_opy_ (u"ࠢࠣࠤࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡶࡸࡦࡸࡴ࠯ࠌࠣࠤࠧࠨࠢ↾")
  if not bs_config:
    return {}
  bstack1111llllll1_opy_ = bstack1l11llll1_opy_(bs_config).bstack1111llll1ll_opy_(bs_config)
  return bstack1111llllll1_opy_
def bstack1ll1l11l1l_opy_(bs_config, framework):
  bstack1lll1111ll_opy_ = False
  bstack1ll111llll_opy_ = False
  bstack1llll1l11111_opy_ = False
  if bstack1111lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ↿") in bs_config:
    bstack1llll1l11111_opy_ = True
  elif bstack1111lll_opy_ (u"ࠩࡤࡴࡵ࠭⇀") in bs_config:
    bstack1lll1111ll_opy_ = True
  else:
    bstack1ll111llll_opy_ = True
  bstack11111ll1_opy_ = {
    bstack1111lll_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⇁"): bstack1ll11l1ll1_opy_.bstack1llll11l1l1l_opy_(bs_config, framework),
    bstack1111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⇂"): bstack1llllll1l1_opy_.bstack1l111l111_opy_(bs_config),
    bstack1111lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⇃"): bs_config.get(bstack1111lll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⇄"), False),
    bstack1111lll_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ⇅"): bstack1ll111llll_opy_,
    bstack1111lll_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⇆"): bstack1lll1111ll_opy_,
    bstack1111lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭⇇"): bstack1llll1l11111_opy_
  }
  return bstack11111ll1_opy_
@error_handler(class_method=False)
def bstack1llll1l111l1_opy_(bs_config):
  try:
    bstack1llll11l1lll_opy_ = json.loads(os.getenv(bstack1111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ⇈"), bstack1111lll_opy_ (u"ࠫࢀࢃࠧ⇉")))
    bstack1llll11l1lll_opy_ = bstack1llll11ll111_opy_(bs_config, bstack1llll11l1lll_opy_)
    return {
        bstack1111lll_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧ⇊"): bstack1llll11l1lll_opy_
    }
  except Exception as error:
    logger.error(bstack1111lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ⇋").format(str(error)))
    return {}
def bstack1llll11ll111_opy_(bs_config, bstack1llll11l1lll_opy_):
  if ((bstack1111lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⇌") in bs_config or not bstack11l1111l1l_opy_(bs_config)) and bstack1llllll1l1_opy_.bstack1l111l111_opy_(bs_config)):
    bstack1llll11l1lll_opy_[bstack1111lll_opy_ (u"ࠣ࡫ࡱࡧࡱࡻࡤࡦࡇࡱࡧࡴࡪࡥࡥࡇࡻࡸࡪࡴࡳࡪࡱࡱࠦ⇍")] = True
  return bstack1llll11l1lll_opy_
def bstack1llll1l1l1l1_opy_(array, bstack1llll11ll1ll_opy_, bstack1llll11lll11_opy_):
  result = {}
  for o in array:
    key = o[bstack1llll11ll1ll_opy_]
    result[key] = o[bstack1llll11lll11_opy_]
  return result
def bstack1llll1ll11ll_opy_(bstack1lllll111_opy_=bstack1111lll_opy_ (u"ࠩࠪ⇎")):
  bstack1llll1l1111l_opy_ = bstack1llllll1l1_opy_.on()
  bstack1llll11lllll_opy_ = bstack1ll11l1ll1_opy_.on()
  bstack1llll11ll11l_opy_ = percy.bstack11l1ll11l1_opy_()
  if bstack1llll11ll11l_opy_ and not bstack1llll11lllll_opy_ and not bstack1llll1l1111l_opy_:
    return bstack1lllll111_opy_ not in [bstack1111lll_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ⇏"), bstack1111lll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⇐")]
  elif bstack1llll1l1111l_opy_ and not bstack1llll11lllll_opy_:
    return bstack1lllll111_opy_ not in [bstack1111lll_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⇑"), bstack1111lll_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⇒"), bstack1111lll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⇓")]
  return bstack1llll1l1111l_opy_ or bstack1llll11lllll_opy_ or bstack1llll11ll11l_opy_
@error_handler(class_method=False)
def bstack1llll1lll11l_opy_(bstack1lllll111_opy_, test=None):
  bstack1llll11lll1l_opy_ = bstack1llllll1l1_opy_.on()
  if not bstack1llll11lll1l_opy_ or bstack1lllll111_opy_ not in [bstack1111lll_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⇔")] or test == None:
    return None
  return {
    bstack1111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⇕"): bstack1llll11lll1l_opy_ and bstack1l11l1l1ll_opy_(threading.current_thread(), bstack1111lll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⇖"), None) == True and bstack1llllll1l1_opy_.bstack11llll111l_opy_(test[bstack1111lll_opy_ (u"ࠫࡹࡧࡧࡴࠩ⇗")])
  }
def bstack1llll11ll1l1_opy_(bs_config, framework):
  bstack1lll1111ll_opy_ = False
  bstack1ll111llll_opy_ = False
  bstack1llll1l11111_opy_ = False
  if bstack1111lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⇘") in bs_config:
    bstack1llll1l11111_opy_ = True
  elif bstack1111lll_opy_ (u"࠭ࡡࡱࡲࠪ⇙") in bs_config:
    bstack1lll1111ll_opy_ = True
  else:
    bstack1ll111llll_opy_ = True
  bstack11111ll1_opy_ = {
    bstack1111lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⇚"): bstack1ll11l1ll1_opy_.bstack1llll11l1l1l_opy_(bs_config, framework),
    bstack1111lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⇛"): bstack1llllll1l1_opy_.bstack11l1111l1_opy_(bs_config),
    bstack1111lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⇜"): bs_config.get(bstack1111lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⇝"), False),
    bstack1111lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⇞"): bstack1ll111llll_opy_,
    bstack1111lll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⇟"): bstack1lll1111ll_opy_,
    bstack1111lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ⇠"): bstack1llll1l11111_opy_
  }
  return bstack11111ll1_opy_