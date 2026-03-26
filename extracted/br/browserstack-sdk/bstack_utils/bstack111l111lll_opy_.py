# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111ll1l1ll1_opy_, bstack1ll11l1l11_opy_, get_host_info, bstack1111111lll1_opy_, \
 bstack1111111l11_opy_, bstack1l11lll1_opy_, error_handler, bstack1111l1ll111_opy_, current_time
import bstack_utils.accessibility as a11y
from bstack_utils.bstack1lll111ll_opy_ import bstack1l111111l1_opy_
from bstack_utils.bstack1l11111l1_opy_ import bstack11llll1l_opy_
from bstack_utils.percy import bstack1lll1ll1ll_opy_
from bstack_utils.config import Config
global_config = Config.get_instance()
logger = logging.getLogger(__name__)
percy = bstack1lll1ll1ll_opy_()
@error_handler(class_method=False)
def bstack1ll1l1ll1ll1_opy_(bs_config, bstack1lll111l11_opy_):
  try:
    data = {
        bstack1ll1lll_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬ⚌"): bstack1ll1lll_opy_ (u"࠭ࡪࡴࡱࡱࠫ⚍"),
        bstack1ll1lll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭⚎"): bs_config.get(bstack1ll1lll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭⚏"), bstack1ll1lll_opy_ (u"ࠩࠪ⚐")),
        bstack1ll1lll_opy_ (u"ࠪࡲࡦࡳࡥࠨ⚑"): bs_config.get(bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ⚒"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⚓"): bs_config.get(bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⚔")),
        bstack1ll1lll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ⚕"): bs_config.get(bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ⚖"), bstack1ll1lll_opy_ (u"ࠩࠪ⚗")),
        bstack1ll1lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ⚘"): current_time(),
        bstack1ll1lll_opy_ (u"ࠫࡹࡧࡧࡴࠩ⚙"): bstack1111111lll1_opy_(bs_config),
        bstack1ll1lll_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨ⚚"): get_host_info(),
        bstack1ll1lll_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧ⚛"): bstack1ll11l1l11_opy_(),
        bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⚜"): os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ⚝")),
        bstack1ll1lll_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧ⚞"): os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨ⚟"), False),
        bstack1ll1lll_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭⚠"): bstack111ll1l1ll1_opy_(),
        bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⚡"): bstack1ll1l11llll1_opy_(bs_config),
        bstack1ll1lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡧࡩࡹࡧࡩ࡭ࡵࠪ⚢"): bstack1ll1l1l11l1l_opy_(bstack1lll111l11_opy_),
        bstack1ll1lll_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ⚣"): bstack1ll1l1l111ll_opy_(bs_config, bstack1lll111l11_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ⚤"), bstack1ll1lll_opy_ (u"ࠩࠪ⚥"))),
        bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⚦"): bstack1111111l11_opy_(bs_config),
        bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠩ⚧"): bstack1ll1l1l1l111_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1ll1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨ⚨").format(str(error)))
    return None
def bstack1ll1l1l11l1l_opy_(framework):
  return {
    bstack1ll1lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭⚩"): framework.get(bstack1ll1lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨ⚪"), bstack1ll1lll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ⚫")),
    bstack1ll1lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ⚬"): framework.get(bstack1ll1lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⚭")),
    bstack1ll1lll_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⚮"): framework.get(bstack1ll1lll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ⚯")),
    bstack1ll1lll_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ⚰"): bstack1ll1lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ⚱"),
    bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⚲"): framework.get(bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⚳"))
  }
def bstack1ll1l1l1l111_opy_(bs_config):
  bstack1ll1lll_opy_ (u"ࠥࠦࠧࠐࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡢࡶ࡫࡯ࡨࠥࡹࡴࡢࡴࡷ࠲ࠏࠦࠠࠣࠤࠥ⚴")
  if not bs_config:
    return {}
  bstack1llll1l111l1_opy_ = bstack1l111111l1_opy_(bs_config).bstack1llll11ll1ll_opy_(bs_config)
  return bstack1llll1l111l1_opy_
def bstack1ll1l1ll1_opy_(bs_config, framework):
  bstack11111l11l_opy_ = False
  bstack111111ll1_opy_ = False
  bstack1ll1l11lllll_opy_ = False
  if bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⚵") in bs_config:
    bstack1ll1l11lllll_opy_ = True
  elif bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱࠩ⚶") in bs_config:
    bstack11111l11l_opy_ = True
  else:
    bstack111111ll1_opy_ = True
  bstack11l1ll1l11_opy_ = {
    bstack1ll1lll_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⚷"): bstack11llll1l_opy_.bstack1ll1l1l1l11l_opy_(bs_config, framework),
    bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⚸"): a11y.is_enabled_root(bs_config),
    bstack1ll1lll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⚹"): bs_config.get(bstack1ll1lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⚺"), False),
    bstack1ll1lll_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⚻"): bstack111111ll1_opy_,
    bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ⚼"): bstack11111l11l_opy_,
    bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ⚽"): bstack1ll1l11lllll_opy_
  }
  return bstack11l1ll1l11_opy_
@error_handler(class_method=False)
def bstack1ll1l11llll1_opy_(bs_config):
  try:
    bstack1ll1l1l11ll1_opy_ = json.loads(os.getenv(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ⚾"), bstack1ll1lll_opy_ (u"ࠧࡼࡿࠪ⚿")))
    bstack1ll1l1l11ll1_opy_ = bstack1ll1l11lll11_opy_(bs_config, bstack1ll1l1l11ll1_opy_)
    return {
        bstack1ll1lll_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪ⛀"): bstack1ll1l1l11ll1_opy_
    }
  except Exception as error:
    logger.error(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡷࡪࡺࡴࡪࡰࡪࡷࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ⛁").format(str(error)))
    return {}
def bstack1ll1l11lll11_opy_(bs_config, bstack1ll1l1l11ll1_opy_):
  if ((bstack1ll1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⛂") in bs_config or not bstack1111111l11_opy_(bs_config)) and a11y.is_enabled_root(bs_config)):
    bstack1ll1l1l11ll1_opy_[bstack1ll1lll_opy_ (u"ࠦ࡮ࡴࡣ࡭ࡷࡧࡩࡊࡴࡣࡰࡦࡨࡨࡊࡾࡴࡦࡰࡶ࡭ࡴࡴࠢ⛃")] = True
  return bstack1ll1l1l11ll1_opy_
def bstack1ll1l1lll11l_opy_(array, bstack1ll1l11lll1l_opy_, bstack1ll1l1l111l1_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1l11lll1l_opy_]
    result[key] = o[bstack1ll1l1l111l1_opy_]
  return result
def bstack1ll1l1ll1l11_opy_(bstack111l1ll1ll_opy_=bstack1ll1lll_opy_ (u"ࠬ࠭⛄")):
  bstack1ll1l1l11111_opy_ = a11y.on()
  bstack1ll1l1l1111l_opy_ = bstack11llll1l_opy_.on()
  bstack1ll1l1l11l11_opy_ = percy.bstack11l1l1lll_opy_()
  if bstack1ll1l1l11l11_opy_ and not bstack1ll1l1l1111l_opy_ and not bstack1ll1l1l11111_opy_:
    return bstack111l1ll1ll_opy_ not in [bstack1ll1lll_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪ⛅"), bstack1ll1lll_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⛆")]
  elif bstack1ll1l1l11111_opy_ and not bstack1ll1l1l1111l_opy_:
    return bstack111l1ll1ll_opy_ not in [bstack1ll1lll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⛇"), bstack1ll1lll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⛈"), bstack1ll1lll_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⛉")]
  return bstack1ll1l1l11111_opy_ or bstack1ll1l1l1111l_opy_ or bstack1ll1l1l11l11_opy_
@error_handler(class_method=False)
def bstack1ll1l1llll1l_opy_(bstack111l1ll1ll_opy_, test=None):
  bstack1ll1l1l11lll_opy_ = a11y.on()
  if not bstack1ll1l1l11lll_opy_ or bstack111l1ll1ll_opy_ not in [bstack1ll1lll_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⛊"), bstack1ll1lll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⛋"), bstack1ll1lll_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪ⛌")] or test == None:
    return None
  return {
    bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⛍"): bstack1ll1l1l11lll_opy_ and bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⛎"), None) == True and a11y.is_enabled_testcase(test.get(bstack1ll1lll_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⛏"), []))
  }
def bstack1ll1l1l111ll_opy_(bs_config, framework):
  bstack11111l11l_opy_ = False
  bstack111111ll1_opy_ = False
  bstack1ll1l11lllll_opy_ = False
  if bstack1ll1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⛐") in bs_config:
    bstack1ll1l11lllll_opy_ = True
  elif bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰࠨ⛑") in bs_config:
    bstack11111l11l_opy_ = True
  else:
    bstack111111ll1_opy_ = True
  bstack11l1ll1l11_opy_ = {
    bstack1ll1lll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⛒"): bstack11llll1l_opy_.bstack1ll1l1l1l11l_opy_(bs_config, framework),
    bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⛓"): a11y.bstack11ll11ll_opy_(bs_config),
    bstack1ll1lll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⛔"): bs_config.get(bstack1ll1lll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⛕"), False),
    bstack1ll1lll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⛖"): bstack111111ll1_opy_,
    bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ⛗"): bstack11111l11l_opy_,
    bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⛘"): bstack1ll1l11lllll_opy_
  }
  return bstack11l1ll1l11_opy_