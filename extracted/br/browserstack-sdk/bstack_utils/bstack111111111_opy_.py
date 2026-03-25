# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111ll11l1l1_opy_, bstack11l1l111ll_opy_, get_host_info, bstack11111llll11_opy_, \
 bstack111l11ll_opy_, bstack1l1lll111l_opy_, error_handler, bstack11111l1111l_opy_, current_time
import bstack_utils.accessibility as a11y
from bstack_utils.bstack1l11llll1l_opy_ import bstack1ll1lll1l_opy_
from bstack_utils.bstack1llll11lll_opy_ import bstack1111l1lll1_opy_
from bstack_utils.percy import bstack1l11111l11_opy_
from bstack_utils.config import Config
global_config = Config.get_instance()
logger = logging.getLogger(__name__)
percy = bstack1l11111l11_opy_()
@error_handler(class_method=False)
def bstack1ll1ll111111_opy_(bs_config, bstack11lll11l11_opy_):
  try:
    data = {
        bstack1l1_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬ♰"): bstack1l1_opy_ (u"࠭ࡪࡴࡱࡱࠫ♱"),
        bstack1l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭♲"): bs_config.get(bstack1l1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭♳"), bstack1l1_opy_ (u"ࠩࠪ♴")),
        bstack1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ♵"): bs_config.get(bstack1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ♶"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ♷"): bs_config.get(bstack1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ♸")),
        bstack1l1_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ♹"): bs_config.get(bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ♺"), bstack1l1_opy_ (u"ࠩࠪ♻")),
        bstack1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧ♼"): current_time(),
        bstack1l1_opy_ (u"ࠫࡹࡧࡧࡴࠩ♽"): bstack11111llll11_opy_(bs_config),
        bstack1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨ♾"): get_host_info(),
        bstack1l1_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧ♿"): bstack11l1l111ll_opy_(),
        bstack1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⚀"): os.environ.get(bstack1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ⚁")),
        bstack1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧ⚂"): os.environ.get(bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨ⚃"), False),
        bstack1l1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭⚄"): bstack111ll11l1l1_opy_(),
        bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⚅"): bstack1ll1l1ll111l_opy_(bs_config),
        bstack1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡧࡩࡹࡧࡩ࡭ࡵࠪ⚆"): bstack1ll1l1l11l11_opy_(bstack11lll11l11_opy_),
        bstack1l1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ⚇"): bstack1ll1l1ll1111_opy_(bs_config, bstack11lll11l11_opy_.get(bstack1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ⚈"), bstack1l1_opy_ (u"ࠩࠪ⚉"))),
        bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⚊"): bstack111l11ll_opy_(bs_config),
        bstack1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠩ⚋"): bstack1ll1l1l1l111_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨ⚌").format(str(error)))
    return None
def bstack1ll1l1l11l11_opy_(framework):
  return {
    bstack1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭⚍"): framework.get(bstack1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨ⚎"), bstack1l1_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ⚏")),
    bstack1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ⚐"): framework.get(bstack1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⚑")),
    bstack1l1_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⚒"): framework.get(bstack1l1_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ⚓")),
    bstack1l1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ⚔"): bstack1l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ⚕"),
    bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⚖"): framework.get(bstack1l1_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⚗"))
  }
def bstack1ll1l1l1l111_opy_(bs_config):
  bstack1l1_opy_ (u"ࠥࠦࠧࠐࠠࠡࡔࡨࡸࡺࡸ࡮ࡴࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠤࡩࡧࡴࡢࠢࡩࡳࡷࠦࡢࡶ࡫࡯ࡨࠥࡹࡴࡢࡴࡷ࠲ࠏࠦࠠࠣࠤࠥ⚘")
  if not bs_config:
    return {}
  bstack1llll1ll1111_opy_ = bstack1ll1lll1l_opy_(bs_config).bstack1lll1llll1l1_opy_(bs_config)
  return bstack1llll1ll1111_opy_
def bstack111l1ll1l_opy_(bs_config, framework):
  bstack11lll1l1_opy_ = False
  bstack11111lllll_opy_ = False
  bstack1ll1l1l1lll1_opy_ = False
  if bstack1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⚙") in bs_config:
    bstack1ll1l1l1lll1_opy_ = True
  elif bstack1l1_opy_ (u"ࠬࡧࡰࡱࠩ⚚") in bs_config:
    bstack11lll1l1_opy_ = True
  else:
    bstack11111lllll_opy_ = True
  bstack1l1ll111l_opy_ = {
    bstack1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⚛"): bstack1111l1lll1_opy_.bstack1ll1l1l1ll11_opy_(bs_config, framework),
    bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⚜"): a11y.is_enabled_root(bs_config),
    bstack1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⚝"): bs_config.get(bstack1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⚞"), False),
    bstack1l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⚟"): bstack11111lllll_opy_,
    bstack1l1_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ⚠"): bstack11lll1l1_opy_,
    bstack1l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ⚡"): bstack1ll1l1l1lll1_opy_
  }
  return bstack1l1ll111l_opy_
@error_handler(class_method=False)
def bstack1ll1l1ll111l_opy_(bs_config):
  try:
    bstack1ll1l1l11lll_opy_ = json.loads(os.getenv(bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ⚢"), bstack1l1_opy_ (u"ࠧࡼࡿࠪ⚣")))
    bstack1ll1l1l11lll_opy_ = bstack1ll1l1l1l11l_opy_(bs_config, bstack1ll1l1l11lll_opy_)
    return {
        bstack1l1_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪ⚤"): bstack1ll1l1l11lll_opy_
    }
  except Exception as error:
    logger.error(bstack1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡷࡪࡺࡴࡪࡰࡪࡷࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ⚥").format(str(error)))
    return {}
def bstack1ll1l1l1l11l_opy_(bs_config, bstack1ll1l1l11lll_opy_):
  if ((bstack1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⚦") in bs_config or not bstack111l11ll_opy_(bs_config)) and a11y.is_enabled_root(bs_config)):
    bstack1ll1l1l11lll_opy_[bstack1l1_opy_ (u"ࠦ࡮ࡴࡣ࡭ࡷࡧࡩࡊࡴࡣࡰࡦࡨࡨࡊࡾࡴࡦࡰࡶ࡭ࡴࡴࠢ⚧")] = True
  return bstack1ll1l1l11lll_opy_
def bstack1ll1l1ll1l11_opy_(array, bstack1ll1l1l1llll_opy_, bstack1ll1l1l11l1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1l1l1llll_opy_]
    result[key] = o[bstack1ll1l1l11l1l_opy_]
  return result
def bstack1ll1l1lll1ll_opy_(bstack1l1111111l_opy_=bstack1l1_opy_ (u"ࠬ࠭⚨")):
  bstack1ll1l1l11ll1_opy_ = a11y.on()
  bstack1ll1l1l1l1ll_opy_ = bstack1111l1lll1_opy_.on()
  bstack1ll1l1l1l1l1_opy_ = percy.bstack1lll1111_opy_()
  if bstack1ll1l1l1l1l1_opy_ and not bstack1ll1l1l1l1ll_opy_ and not bstack1ll1l1l11ll1_opy_:
    return bstack1l1111111l_opy_ not in [bstack1l1_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪ⚩"), bstack1l1_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⚪")]
  elif bstack1ll1l1l11ll1_opy_ and not bstack1ll1l1l1l1ll_opy_:
    return bstack1l1111111l_opy_ not in [bstack1l1_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⚫"), bstack1l1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⚬"), bstack1l1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⚭")]
  return bstack1ll1l1l11ll1_opy_ or bstack1ll1l1l1l1ll_opy_ or bstack1ll1l1l1l1l1_opy_
@error_handler(class_method=False)
def bstack1ll1ll111l11_opy_(bstack1l1111111l_opy_, test=None):
  bstack1ll1l1l1ll1l_opy_ = a11y.on()
  if not bstack1ll1l1l1ll1l_opy_ or bstack1l1111111l_opy_ not in [bstack1l1_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ⚮"), bstack1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⚯"), bstack1l1_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪ⚰")] or test == None:
    return None
  return {
    bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⚱"): bstack1ll1l1l1ll1l_opy_ and bstack1l1lll111l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⚲"), None) == True and a11y.is_enabled_testcase(test.get(bstack1l1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⚳"), []))
  }
def bstack1ll1l1ll1111_opy_(bs_config, framework):
  bstack11lll1l1_opy_ = False
  bstack11111lllll_opy_ = False
  bstack1ll1l1l1lll1_opy_ = False
  if bstack1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⚴") in bs_config:
    bstack1ll1l1l1lll1_opy_ = True
  elif bstack1l1_opy_ (u"ࠫࡦࡶࡰࠨ⚵") in bs_config:
    bstack11lll1l1_opy_ = True
  else:
    bstack11111lllll_opy_ = True
  bstack1l1ll111l_opy_ = {
    bstack1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⚶"): bstack1111l1lll1_opy_.bstack1ll1l1l1ll11_opy_(bs_config, framework),
    bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⚷"): a11y.bstack1l11ll1l1_opy_(bs_config),
    bstack1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⚸"): bs_config.get(bstack1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⚹"), False),
    bstack1l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⚺"): bstack11111lllll_opy_,
    bstack1l1_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ⚻"): bstack11lll1l1_opy_,
    bstack1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⚼"): bstack1ll1l1l1lll1_opy_
  }
  return bstack1l1ll111l_opy_