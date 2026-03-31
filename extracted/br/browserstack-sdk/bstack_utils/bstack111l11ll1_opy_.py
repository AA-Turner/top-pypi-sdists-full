# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111ll1lllll_opy_, bstack11ll11l1l1_opy_, get_host_info, bstack111111l11ll_opy_, \
 bstack1ll11l1l11_opy_, bstack1l1111l111_opy_, error_handler, bstack111111l1111_opy_, current_time
import bstack_utils.accessibility as a11y
from bstack_utils.bstack1l1l1llll1_opy_ import bstack1l1ll11ll1_opy_
from bstack_utils.bstack111l111l_opy_ import bstack11l11l1lll_opy_
from bstack_utils.percy import bstack1l1l1ll1l1_opy_
from bstack_utils.config import Config
global_config = Config.get_instance()
logger = logging.getLogger(__name__)
percy = bstack1l1l1ll1l1_opy_()
@error_handler(class_method=False)
def bstack1ll1l1ll1ll1_opy_(bs_config, bstack1l111ll1l1_opy_):
  try:
    data = {
        bstack1ll11_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨ⚝"): bstack1ll11_opy_ (u"ࠩ࡭ࡷࡴࡴࠧ⚞"),
        bstack1ll11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩ⚟"): bs_config.get(bstack1ll11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ⚠"), bstack1ll11_opy_ (u"ࠬ࠭⚡")),
        bstack1ll11_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ⚢"): bs_config.get(bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ⚣"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⚤"): bs_config.get(bstack1ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⚥")),
        bstack1ll11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ⚦"): bs_config.get(bstack1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ⚧"), bstack1ll11_opy_ (u"ࠬ࠭⚨")),
        bstack1ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ⚩"): current_time(),
        bstack1ll11_opy_ (u"ࠧࡵࡣࡪࡷࠬ⚪"): bstack111111l11ll_opy_(bs_config),
        bstack1ll11_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫ⚫"): get_host_info(),
        bstack1ll11_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪ⚬"): bstack11ll11l1l1_opy_(),
        bstack1ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⚭"): os.environ.get(bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ⚮")),
        bstack1ll11_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪ⚯"): os.environ.get(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ⚰"), False),
        bstack1ll11_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩ⚱"): bstack111ll1lllll_opy_(),
        bstack1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⚲"): bstack1ll1l1l11111_opy_(bs_config),
        bstack1ll11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭⚳"): bstack1ll1l11lll11_opy_(bstack1l111ll1l1_opy_),
        bstack1ll11_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ⚴"): bstack1ll1l11llll1_opy_(bs_config, bstack1l111ll1l1_opy_.get(bstack1ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ⚵"), bstack1ll11_opy_ (u"ࠬ࠭⚶"))),
        bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ⚷"): bstack1ll11l1l11_opy_(bs_config),
        bstack1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡤࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠬ⚸"): bstack1ll1l1l11lll_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤ⚹").format(str(error)))
    return None
def bstack1ll1l11lll11_opy_(framework):
  return {
    bstack1ll11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩ⚺"): framework.get(bstack1ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫ⚻"), bstack1ll11_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ⚼")),
    bstack1ll11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⚽"): framework.get(bstack1ll11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ⚾")),
    bstack1ll11_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ⚿"): framework.get(bstack1ll11_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⛀")),
    bstack1ll11_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ⛁"): bstack1ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⛂"),
    bstack1ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⛃"): framework.get(bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⛄"))
  }
def bstack1ll1l1l11lll_opy_(bs_config):
  bstack1ll11_opy_ (u"ࠨࠢࠣࠌࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡵࡷࡥࡷࡺ࠮ࠋࠢࠣࠦࠧࠨ⛅")
  if not bs_config:
    return {}
  bstack1llll1111lll_opy_ = bstack1l1ll11ll1_opy_(bs_config).bstack1llll1l111ll_opy_(bs_config)
  return bstack1llll1111lll_opy_
def bstack11ll1l111_opy_(bs_config, framework):
  bstack11l1llll1l_opy_ = False
  bstack11111lll_opy_ = False
  bstack1ll1l11lll1l_opy_ = False
  if bstack1ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⛆") in bs_config:
    bstack1ll1l11lll1l_opy_ = True
  elif bstack1ll11_opy_ (u"ࠨࡣࡳࡴࠬ⛇") in bs_config:
    bstack11l1llll1l_opy_ = True
  else:
    bstack11111lll_opy_ = True
  bstack1ll1lll11_opy_ = {
    bstack1ll11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⛈"): bstack11l11l1lll_opy_.bstack1ll1l1l111l1_opy_(bs_config, framework),
    bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⛉"): a11y.is_enabled_root(bs_config),
    bstack1ll11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⛊"): bs_config.get(bstack1ll11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⛋"), False),
    bstack1ll11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⛌"): bstack11111lll_opy_,
    bstack1ll11_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⛍"): bstack11l1llll1l_opy_,
    bstack1ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ⛎"): bstack1ll1l11lll1l_opy_
  }
  return bstack1ll1lll11_opy_
@error_handler(class_method=False)
def bstack1ll1l1l11111_opy_(bs_config):
  try:
    bstack1ll1l1l11l11_opy_ = json.loads(os.getenv(bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ⛏"), bstack1ll11_opy_ (u"ࠪࡿࢂ࠭⛐")))
    bstack1ll1l1l11l11_opy_ = bstack1ll1l1l11ll1_opy_(bs_config, bstack1ll1l1l11l11_opy_)
    return {
        bstack1ll11_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭⛑"): bstack1ll1l1l11l11_opy_
    }
  except Exception as error:
    logger.error(bstack1ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦ⛒").format(str(error)))
    return {}
def bstack1ll1l1l11ll1_opy_(bs_config, bstack1ll1l1l11l11_opy_):
  if ((bstack1ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⛓") in bs_config or not bstack1ll11l1l11_opy_(bs_config)) and a11y.is_enabled_root(bs_config)):
    bstack1ll1l1l11l11_opy_[bstack1ll11_opy_ (u"ࠢࡪࡰࡦࡰࡺࡪࡥࡆࡰࡦࡳࡩ࡫ࡤࡆࡺࡷࡩࡳࡹࡩࡰࡰࠥ⛔")] = True
  return bstack1ll1l1l11l11_opy_
def bstack1ll1l1lllll1_opy_(array, bstack1ll1l11ll1ll_opy_, bstack1ll1l1l111ll_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1l11ll1ll_opy_]
    result[key] = o[bstack1ll1l1l111ll_opy_]
  return result
def bstack1ll1l1lll1ll_opy_(bstack1l1ll111l_opy_=bstack1ll11_opy_ (u"ࠨࠩ⛕")):
  bstack1ll1l11lllll_opy_ = a11y.on()
  bstack1ll1l11ll1l1_opy_ = bstack11l11l1lll_opy_.on()
  bstack1ll1l1l11l1l_opy_ = percy.bstack1lllll1l1_opy_()
  if bstack1ll1l1l11l1l_opy_ and not bstack1ll1l11ll1l1_opy_ and not bstack1ll1l11lllll_opy_:
    return bstack1l1ll111l_opy_ not in [bstack1ll11_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭⛖"), bstack1ll11_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⛗")]
  elif bstack1ll1l11lllll_opy_ and not bstack1ll1l11ll1l1_opy_:
    return bstack1l1ll111l_opy_ not in [bstack1ll11_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⛘"), bstack1ll11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⛙"), bstack1ll11_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ⛚")]
  return bstack1ll1l11lllll_opy_ or bstack1ll1l11ll1l1_opy_ or bstack1ll1l1l11l1l_opy_
@error_handler(class_method=False)
def bstack1ll1l1llll11_opy_(bstack1l1ll111l_opy_, test=None):
  bstack1ll1l1l1111l_opy_ = a11y.on()
  if not bstack1ll1l1l1111l_opy_ or bstack1l1ll111l_opy_ not in [bstack1ll11_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⛛"), bstack1ll11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⛜"), bstack1ll11_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭⛝")] or test == None:
    return None
  return {
    bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⛞"): bstack1ll1l1l1111l_opy_ and bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⛟"), None) == True and a11y.is_enabled_testcase(test.get(bstack1ll11_opy_ (u"ࠬࡺࡡࡨࡵࠪ⛠"), []))
  }
def bstack1ll1l11llll1_opy_(bs_config, framework):
  bstack11l1llll1l_opy_ = False
  bstack11111lll_opy_ = False
  bstack1ll1l11lll1l_opy_ = False
  if bstack1ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⛡") in bs_config:
    bstack1ll1l11lll1l_opy_ = True
  elif bstack1ll11_opy_ (u"ࠧࡢࡲࡳࠫ⛢") in bs_config:
    bstack11l1llll1l_opy_ = True
  else:
    bstack11111lll_opy_ = True
  bstack1ll1lll11_opy_ = {
    bstack1ll11_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⛣"): bstack11l11l1lll_opy_.bstack1ll1l1l111l1_opy_(bs_config, framework),
    bstack1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⛤"): a11y.bstack1111l1llll_opy_(bs_config),
    bstack1ll11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⛥"): bs_config.get(bstack1ll11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⛦"), False),
    bstack1ll11_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⛧"): bstack11111lll_opy_,
    bstack1ll11_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⛨"): bstack11l1llll1l_opy_,
    bstack1ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ⛩"): bstack1ll1l11lll1l_opy_
  }
  return bstack1ll1lll11_opy_