# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111lll11lll_opy_, bstack1l1l1ll1l_opy_, get_host_info, bstack1111l111ll1_opy_, \
 bstack1l111llll_opy_, bstack111l1lll11_opy_, error_handler, bstack1llllllll1ll_opy_, current_time
import bstack_utils.accessibility as a11y
from bstack_utils.bstack1lll11llll_opy_ import bstack1l11ll1ll1_opy_
from bstack_utils.bstack11111l11_opy_ import bstack11lll1l11_opy_
from bstack_utils.percy import bstack1l11lll1ll_opy_
from bstack_utils.config import Config
global_config = Config.get_instance()
logger = logging.getLogger(__name__)
percy = bstack1l11lll1ll_opy_()
@error_handler(class_method=False)
def bstack1ll1ll111l1l_opy_(bs_config, bstack1l1ll11l11_opy_):
  try:
    data = {
        bstack1ll1lll_opy_ (u"ࠧࡧࡱࡵࡱࡦࡺࠧ♫"): bstack1ll1lll_opy_ (u"ࠨ࡬ࡶࡳࡳ࠭♬"),
        bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡢࡲࡦࡳࡥࠨ♭"): bs_config.get(bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ♮"), bstack1ll1lll_opy_ (u"ࠫࠬ♯")),
        bstack1ll1lll_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ♰"): bs_config.get(bstack1ll1lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ♱"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1ll1lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ♲"): bs_config.get(bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ♳")),
        bstack1ll1lll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ♴"): bs_config.get(bstack1ll1lll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭♵"), bstack1ll1lll_opy_ (u"ࠫࠬ♶")),
        bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ♷"): current_time(),
        bstack1ll1lll_opy_ (u"࠭ࡴࡢࡩࡶࠫ♸"): bstack1111l111ll1_opy_(bs_config),
        bstack1ll1lll_opy_ (u"ࠧࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠪ♹"): get_host_info(),
        bstack1ll1lll_opy_ (u"ࠨࡥ࡬ࡣ࡮ࡴࡦࡰࠩ♺"): bstack1l1l1ll1l_opy_(),
        bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡴࡸࡲࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ♻"): os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ♼")),
        bstack1ll1lll_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡸࡵ࡯ࠩ♽"): os.environ.get(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪ♾"), False),
        bstack1ll1lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡤࡱࡱࡸࡷࡵ࡬ࠨ♿"): bstack111lll11lll_opy_(),
        bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⚀"): bstack1ll1l1ll1111_opy_(bs_config),
        bstack1ll1lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠬ⚁"): bstack1ll1l1l1l1l1_opy_(bstack1l1ll11l11_opy_),
        bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ⚂"): bstack1ll1l1l1l11l_opy_(bs_config, bstack1l1ll11l11_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫ⚃"), bstack1ll1lll_opy_ (u"ࠫࠬ⚄"))),
        bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ⚅"): bstack1l111llll_opy_(bs_config),
        bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡣࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠫ⚆"): bstack1ll1l1ll111l_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1ll1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ⚇").format(str(error)))
    return None
def bstack1ll1l1l1l1l1_opy_(framework):
  return {
    bstack1ll1lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ⚈"): framework.get(bstack1ll1lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ⚉"), bstack1ll1lll_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ⚊")),
    bstack1ll1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ⚋"): framework.get(bstack1ll1lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⚌")),
    bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ⚍"): framework.get(bstack1ll1lll_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⚎")),
    bstack1ll1lll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ⚏"): bstack1ll1lll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ⚐"),
    bstack1ll1lll_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⚑"): framework.get(bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⚒"))
  }
def bstack1ll1l1ll111l_opy_(bs_config):
  bstack1ll1lll_opy_ (u"ࠧࠨࠢࠋࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡴࡶࡤࡶࡹ࠴ࠊࠡࠢࠥࠦࠧ⚓")
  if not bs_config:
    return {}
  bstack1llll1l1l111_opy_ = bstack1l11ll1ll1_opy_(bs_config).bstack1llll11ll1l1_opy_(bs_config)
  return bstack1llll1l1l111_opy_
def bstack11ll111ll1_opy_(bs_config, framework):
  bstack1ll11111l1_opy_ = False
  bstack1l1111ll1l_opy_ = False
  bstack1ll1l1l11ll1_opy_ = False
  if bstack1ll1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⚔") in bs_config:
    bstack1ll1l1l11ll1_opy_ = True
  elif bstack1ll1lll_opy_ (u"ࠧࡢࡲࡳࠫ⚕") in bs_config:
    bstack1ll11111l1_opy_ = True
  else:
    bstack1l1111ll1l_opy_ = True
  bstack11l11l111l_opy_ = {
    bstack1ll1lll_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⚖"): bstack11lll1l11_opy_.bstack1ll1l1l1l111_opy_(bs_config, framework),
    bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⚗"): a11y.is_enabled_root(bs_config),
    bstack1ll1lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⚘"): bs_config.get(bstack1ll1lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⚙"), False),
    bstack1ll1lll_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⚚"): bstack1l1111ll1l_opy_,
    bstack1ll1lll_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⚛"): bstack1ll11111l1_opy_,
    bstack1ll1lll_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ⚜"): bstack1ll1l1l11ll1_opy_
  }
  return bstack11l11l111l_opy_
@error_handler(class_method=False)
def bstack1ll1l1ll1111_opy_(bs_config):
  try:
    bstack1ll1l1l1ll11_opy_ = json.loads(os.getenv(bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ⚝"), bstack1ll1lll_opy_ (u"ࠩࡾࢁࠬ⚞")))
    bstack1ll1l1l1ll11_opy_ = bstack1ll1l1l1lll1_opy_(bs_config, bstack1ll1l1l1ll11_opy_)
    return {
        bstack1ll1lll_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬ⚟"): bstack1ll1l1l1ll11_opy_
    }
  except Exception as error:
    logger.error(bstack1ll1lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥ⚠").format(str(error)))
    return {}
def bstack1ll1l1l1lll1_opy_(bs_config, bstack1ll1l1l1ll11_opy_):
  if ((bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⚡") in bs_config or not bstack1l111llll_opy_(bs_config)) and a11y.is_enabled_root(bs_config)):
    bstack1ll1l1l1ll11_opy_[bstack1ll1lll_opy_ (u"ࠨࡩ࡯ࡥ࡯ࡹࡩ࡫ࡅ࡯ࡥࡲࡨࡪࡪࡅࡹࡶࡨࡲࡸ࡯࡯࡯ࠤ⚢")] = True
  return bstack1ll1l1l1ll11_opy_
def bstack1ll1ll111l11_opy_(array, bstack1ll1l1ll11l1_opy_, bstack1ll1l1l1llll_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1l1ll11l1_opy_]
    result[key] = o[bstack1ll1l1l1llll_opy_]
  return result
def bstack1ll1l1ll1l11_opy_(bstack111111ll11_opy_=bstack1ll1lll_opy_ (u"ࠧࠨ⚣")):
  bstack1ll1l1l1l1ll_opy_ = a11y.on()
  bstack1ll1l1l1ll1l_opy_ = bstack11lll1l11_opy_.on()
  bstack1ll1l1l11lll_opy_ = percy.bstack1l1l11ll11_opy_()
  if bstack1ll1l1l11lll_opy_ and not bstack1ll1l1l1ll1l_opy_ and not bstack1ll1l1l1l1ll_opy_:
    return bstack111111ll11_opy_ not in [bstack1ll1lll_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬ⚤"), bstack1ll1lll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭⚥")]
  elif bstack1ll1l1l1l1ll_opy_ and not bstack1ll1l1l1ll1l_opy_:
    return bstack111111ll11_opy_ not in [bstack1ll1lll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⚦"), bstack1ll1lll_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⚧"), bstack1ll1lll_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⚨")]
  return bstack1ll1l1l1l1ll_opy_ or bstack1ll1l1l1ll1l_opy_ or bstack1ll1l1l11lll_opy_
@error_handler(class_method=False)
def bstack1ll1ll11l11l_opy_(bstack111111ll11_opy_, test=None):
  bstack1ll1l1l11l1l_opy_ = a11y.on()
  if not bstack1ll1l1l11l1l_opy_ or bstack111111ll11_opy_ not in [bstack1ll1lll_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⚩"), bstack1ll1lll_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⚪"), bstack1ll1lll_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬ⚫")] or test == None:
    return None
  return {
    bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⚬"): bstack1ll1l1l11l1l_opy_ and bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ⚭"), None) == True and a11y.is_enabled_testcase(test.get(bstack1ll1lll_opy_ (u"ࠫࡹࡧࡧࡴࠩ⚮"), []))
  }
def bstack1ll1l1l1l11l_opy_(bs_config, framework):
  bstack1ll11111l1_opy_ = False
  bstack1l1111ll1l_opy_ = False
  bstack1ll1l1l11ll1_opy_ = False
  if bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⚯") in bs_config:
    bstack1ll1l1l11ll1_opy_ = True
  elif bstack1ll1lll_opy_ (u"࠭ࡡࡱࡲࠪ⚰") in bs_config:
    bstack1ll11111l1_opy_ = True
  else:
    bstack1l1111ll1l_opy_ = True
  bstack11l11l111l_opy_ = {
    bstack1ll1lll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⚱"): bstack11lll1l11_opy_.bstack1ll1l1l1l111_opy_(bs_config, framework),
    bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⚲"): a11y.bstack1l1ll111ll_opy_(bs_config),
    bstack1ll1lll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⚳"): bs_config.get(bstack1ll1lll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⚴"), False),
    bstack1ll1lll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⚵"): bstack1l1111ll1l_opy_,
    bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⚶"): bstack1ll11111l1_opy_,
    bstack1ll1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ⚷"): bstack1ll1l1l11ll1_opy_
  }
  return bstack11l11l111l_opy_