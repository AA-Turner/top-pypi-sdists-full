# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111ll1ll111_opy_, bstack11l111111_opy_, get_host_info, bstack1lllllllllll_opy_, \
 bstack1ll111l11l_opy_, bstack111ll1ll_opy_, error_handler, bstack1111l1l1l11_opy_, current_time
import bstack_utils.accessibility as a11y
from bstack_utils.bstack1111ll1l_opy_ import bstack11lllllll_opy_
from bstack_utils.bstack1llll11l11_opy_ import bstack1ll1l1l1l1_opy_
from bstack_utils.percy import bstack1l1ll11l11_opy_
from bstack_utils.config import Config
global_config = Config.get_instance()
logger = logging.getLogger(__name__)
percy = bstack1l1ll11l11_opy_()
@error_handler(class_method=False)
def bstack1ll1ll11l1ll_opy_(bs_config, bstack1l11l11l1l_opy_):
  try:
    data = {
        bstack11lll1_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨ♥"): bstack11lll1_opy_ (u"ࠩ࡭ࡷࡴࡴࠧ♦"),
        bstack11lll1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩ♧"): bs_config.get(bstack11lll1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ♨"), bstack11lll1_opy_ (u"ࠬ࠭♩")),
        bstack11lll1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ♪"): bs_config.get(bstack11lll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ♫"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11lll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ♬"): bs_config.get(bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ♭")),
        bstack11lll1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ♮"): bs_config.get(bstack11lll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ♯"), bstack11lll1_opy_ (u"ࠬ࠭♰")),
        bstack11lll1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ♱"): current_time(),
        bstack11lll1_opy_ (u"ࠧࡵࡣࡪࡷࠬ♲"): bstack1lllllllllll_opy_(bs_config),
        bstack11lll1_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫ♳"): get_host_info(),
        bstack11lll1_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪ♴"): bstack11l111111_opy_(),
        bstack11lll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ♵"): os.environ.get(bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ♶")),
        bstack11lll1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪ♷"): os.environ.get(bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ♸"), False),
        bstack11lll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩ♹"): bstack111ll1ll111_opy_(),
        bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ♺"): bstack1ll1l1l1l11l_opy_(bs_config),
        bstack11lll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭♻"): bstack1ll1l1l1l1l1_opy_(bstack1l11l11l1l_opy_),
        bstack11lll1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ♼"): bstack1ll1l1ll11ll_opy_(bs_config, bstack1l11l11l1l_opy_.get(bstack11lll1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ♽"), bstack11lll1_opy_ (u"ࠬ࠭♾"))),
        bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ♿"): bstack1ll111l11l_opy_(bs_config),
        bstack11lll1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠬ⚀"): bstack1ll1l1ll1l11_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack11lll1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤ⚁").format(str(error)))
    return None
def bstack1ll1l1l1l1l1_opy_(framework):
  return {
    bstack11lll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩ⚂"): framework.get(bstack11lll1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫ⚃"), bstack11lll1_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ⚄")),
    bstack11lll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⚅"): framework.get(bstack11lll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ⚆")),
    bstack11lll1_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ⚇"): framework.get(bstack11lll1_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⚈")),
    bstack11lll1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ⚉"): bstack11lll1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ⚊"),
    bstack11lll1_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⚋"): framework.get(bstack11lll1_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⚌"))
  }
def bstack1ll1l1ll1l11_opy_(bs_config):
  bstack11lll1_opy_ (u"ࠨࠢࠣࠌࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡵࡷࡥࡷࡺ࠮ࠋࠢࠣࠦࠧࠨ⚍")
  if not bs_config:
    return {}
  bstack1llll1l1l111_opy_ = bstack11lllllll_opy_(bs_config).bstack1lll1lllll1l_opy_(bs_config)
  return bstack1llll1l1l111_opy_
def bstack11lll11lll_opy_(bs_config, framework):
  bstack111l1l111_opy_ = False
  bstack11llll1l1l_opy_ = False
  bstack1ll1l1l1ll11_opy_ = False
  if bstack11lll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⚎") in bs_config:
    bstack1ll1l1l1ll11_opy_ = True
  elif bstack11lll1_opy_ (u"ࠨࡣࡳࡴࠬ⚏") in bs_config:
    bstack111l1l111_opy_ = True
  else:
    bstack11llll1l1l_opy_ = True
  bstack1ll11l1l11_opy_ = {
    bstack11lll1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⚐"): bstack1ll1l1l1l1_opy_.bstack1ll1l1l1lll1_opy_(bs_config, framework),
    bstack11lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⚑"): a11y.is_enabled_root(bs_config),
    bstack11lll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⚒"): bs_config.get(bstack11lll1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⚓"), False),
    bstack11lll1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⚔"): bstack11llll1l1l_opy_,
    bstack11lll1_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⚕"): bstack111l1l111_opy_,
    bstack11lll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ⚖"): bstack1ll1l1l1ll11_opy_
  }
  return bstack1ll11l1l11_opy_
@error_handler(class_method=False)
def bstack1ll1l1l1l11l_opy_(bs_config):
  try:
    bstack1ll1l1l1l1ll_opy_ = json.loads(os.getenv(bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ⚗"), bstack11lll1_opy_ (u"ࠪࡿࢂ࠭⚘")))
    bstack1ll1l1l1l1ll_opy_ = bstack1ll1l1ll11l1_opy_(bs_config, bstack1ll1l1l1l1ll_opy_)
    return {
        bstack11lll1_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭⚙"): bstack1ll1l1l1l1ll_opy_
    }
  except Exception as error:
    logger.error(bstack11lll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦ⚚").format(str(error)))
    return {}
def bstack1ll1l1ll11l1_opy_(bs_config, bstack1ll1l1l1l1ll_opy_):
  if ((bstack11lll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⚛") in bs_config or not bstack1ll111l11l_opy_(bs_config)) and a11y.is_enabled_root(bs_config)):
    bstack1ll1l1l1l1ll_opy_[bstack11lll1_opy_ (u"ࠢࡪࡰࡦࡰࡺࡪࡥࡆࡰࡦࡳࡩ࡫ࡤࡆࡺࡷࡩࡳࡹࡩࡰࡰࠥ⚜")] = True
  return bstack1ll1l1l1l1ll_opy_
def bstack1ll1ll11l11l_opy_(array, bstack1ll1l1l1llll_opy_, bstack1ll1l1ll1l1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1l1l1llll_opy_]
    result[key] = o[bstack1ll1l1ll1l1l_opy_]
  return result
def bstack1ll1l1llll1l_opy_(bstack111l11lll1_opy_=bstack11lll1_opy_ (u"ࠨࠩ⚝")):
  bstack1ll1l1ll111l_opy_ = a11y.on()
  bstack1ll1l1l1l111_opy_ = bstack1ll1l1l1l1_opy_.on()
  bstack1ll1l1l1ll1l_opy_ = percy.bstack1l1l111l1_opy_()
  if bstack1ll1l1l1ll1l_opy_ and not bstack1ll1l1l1l111_opy_ and not bstack1ll1l1ll111l_opy_:
    return bstack111l11lll1_opy_ not in [bstack11lll1_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭⚞"), bstack11lll1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⚟")]
  elif bstack1ll1l1ll111l_opy_ and not bstack1ll1l1l1l111_opy_:
    return bstack111l11lll1_opy_ not in [bstack11lll1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⚠"), bstack11lll1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⚡"), bstack11lll1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ⚢")]
  return bstack1ll1l1ll111l_opy_ or bstack1ll1l1l1l111_opy_ or bstack1ll1l1l1ll1l_opy_
@error_handler(class_method=False)
def bstack1ll1ll111111_opy_(bstack111l11lll1_opy_, test=None):
  bstack1ll1l1ll1111_opy_ = a11y.on()
  if not bstack1ll1l1ll1111_opy_ or bstack111l11lll1_opy_ not in [bstack11lll1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⚣"), bstack11lll1_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⚤"), bstack11lll1_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭⚥")] or test == None:
    return None
  return {
    bstack11lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⚦"): bstack1ll1l1ll1111_opy_ and bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⚧"), None) == True and a11y.is_enabled_testcase(test.get(bstack11lll1_opy_ (u"ࠬࡺࡡࡨࡵࠪ⚨"), []))
  }
def bstack1ll1l1ll11ll_opy_(bs_config, framework):
  bstack111l1l111_opy_ = False
  bstack11llll1l1l_opy_ = False
  bstack1ll1l1l1ll11_opy_ = False
  if bstack11lll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⚩") in bs_config:
    bstack1ll1l1l1ll11_opy_ = True
  elif bstack11lll1_opy_ (u"ࠧࡢࡲࡳࠫ⚪") in bs_config:
    bstack111l1l111_opy_ = True
  else:
    bstack11llll1l1l_opy_ = True
  bstack1ll11l1l11_opy_ = {
    bstack11lll1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⚫"): bstack1ll1l1l1l1_opy_.bstack1ll1l1l1lll1_opy_(bs_config, framework),
    bstack11lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⚬"): a11y.bstack111ll11l11_opy_(bs_config),
    bstack11lll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⚭"): bs_config.get(bstack11lll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⚮"), False),
    bstack11lll1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⚯"): bstack11llll1l1l_opy_,
    bstack11lll1_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⚰"): bstack111l1l111_opy_,
    bstack11lll1_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ⚱"): bstack1ll1l1l1ll11_opy_
  }
  return bstack1ll11l1l11_opy_