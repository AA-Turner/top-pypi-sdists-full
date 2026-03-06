# coding: UTF-8
import sys
bstack1lllll_opy_ = sys.version_info [0] == 2
bstack1l1ll1_opy_ = 2048
bstack1lllll1l_opy_ = 7
def bstack1111_opy_ (bstack1l11ll1_opy_):
    global bstack1l_opy_
    bstack11lll1l_opy_ = ord (bstack1l11ll1_opy_ [-1])
    bstack1llll1_opy_ = bstack1l11ll1_opy_ [:-1]
    bstack111ll11_opy_ = bstack11lll1l_opy_ % len (bstack1llll1_opy_)
    bstack1111l_opy_ = bstack1llll1_opy_ [:bstack111ll11_opy_] + bstack1llll1_opy_ [bstack111ll11_opy_:]
    if bstack1lllll_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1l1ll1_opy_ - (bstack1l11_opy_ + bstack11lll1l_opy_) % bstack1lllll1l_opy_) for bstack1l11_opy_, char in enumerate (bstack1111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111llllll11_opy_, bstack1ll11111_opy_, get_host_info, bstack1111lll1ll1_opy_, \
 bstack1ll11ll11l_opy_, bstack1lll11lll1_opy_, error_handler, bstack1111l1111ll_opy_, current_time
import bstack_utils.accessibility as bstack11l1111111_opy_
from bstack_utils.bstack1l11111ll1_opy_ import bstack11l111lll1_opy_
from bstack_utils.bstack1111l1l1l1_opy_ import bstack11l111ll11_opy_
from bstack_utils.percy import bstack1l111llll1_opy_
from bstack_utils.config import Config
global_config = Config.get_instance()
logger = logging.getLogger(__name__)
percy = bstack1l111llll1_opy_()
@error_handler(class_method=False)
def bstack1ll1lllll1l1_opy_(bs_config, bstack11l1llll11_opy_):
  try:
    data = {
        bstack1111_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨ╔"): bstack1111_opy_ (u"ࠩ࡭ࡷࡴࡴࠧ╕"),
        bstack1111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩ╖"): bs_config.get(bstack1111_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ╗"), bstack1111_opy_ (u"ࠬ࠭╘")),
        bstack1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ╙"): bs_config.get(bstack1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ╚"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ╛"): bs_config.get(bstack1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ╜")),
        bstack1111_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ╝"): bs_config.get(bstack1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ╞"), bstack1111_opy_ (u"ࠬ࠭╟")),
        bstack1111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ╠"): current_time(),
        bstack1111_opy_ (u"ࠧࡵࡣࡪࡷࠬ╡"): bstack1111lll1ll1_opy_(bs_config),
        bstack1111_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫ╢"): get_host_info(),
        bstack1111_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪ╣"): bstack1ll11111_opy_(),
        bstack1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ╤"): os.environ.get(bstack1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ╥")),
        bstack1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪ╦"): os.environ.get(bstack1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ╧"), False),
        bstack1111_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩ╨"): bstack111llllll11_opy_(),
        bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ╩"): bstack1ll1lll1111l_opy_(bs_config),
        bstack1111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭╪"): bstack1ll1ll1ll11l_opy_(bstack11l1llll11_opy_),
        bstack1111_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ╫"): bstack1ll1ll1l1lll_opy_(bs_config, bstack11l1llll11_opy_.get(bstack1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ╬"), bstack1111_opy_ (u"ࠬ࠭╭"))),
        bstack1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ╮"): bstack1ll11ll11l_opy_(bs_config),
        bstack1111_opy_ (u"ࠧࡵࡧࡶࡸࡤࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠬ╯"): bstack1ll1lll11111_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡶࡡࡺ࡮ࡲࡥࡩࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤ╰").format(str(error)))
    return None
def bstack1ll1ll1ll11l_opy_(framework):
  return {
    bstack1111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩ╱"): framework.get(bstack1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥ࡮ࡢ࡯ࡨࠫ╲"), bstack1111_opy_ (u"ࠫࡕࡿࡴࡦࡵࡷࠫ╳")),
    bstack1111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ╴"): framework.get(bstack1111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ╵")),
    bstack1111_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ╶"): framework.get(bstack1111_opy_ (u"ࠨࡵࡧ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭╷")),
    bstack1111_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ╸"): bstack1111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ╹"),
    bstack1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ╺"): framework.get(bstack1111_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ╻"))
  }
def bstack1ll1lll11111_opy_(bs_config):
  bstack1111_opy_ (u"ࠨࠢࠣࠌࠣࠤࡗ࡫ࡴࡶࡴࡱࡷࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠠࡥࡣࡷࡥࠥ࡬࡯ࡳࠢࡥࡹ࡮ࡲࡤࠡࡵࡷࡥࡷࡺ࠮ࠋࠢࠣࠦࠧࠨ╼")
  if not bs_config:
    return {}
  bstack1lllll1l11ll_opy_ = bstack11l111lll1_opy_(bs_config).bstack1llll1l1ll1l_opy_(bs_config)
  return bstack1lllll1l11ll_opy_
def bstack111l11l1l1_opy_(bs_config, framework):
  bstack11111ll11_opy_ = False
  bstack1111lll1ll_opy_ = False
  bstack1ll1ll1l1l11_opy_ = False
  if bstack1111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ╽") in bs_config:
    bstack1ll1ll1l1l11_opy_ = True
  elif bstack1111_opy_ (u"ࠨࡣࡳࡴࠬ╾") in bs_config:
    bstack11111ll11_opy_ = True
  else:
    bstack1111lll1ll_opy_ = True
  bstack1ll11ll1_opy_ = {
    bstack1111_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ╿"): bstack11l111ll11_opy_.bstack1ll1ll1llll1_opy_(bs_config, framework),
    bstack1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ▀"): bstack11l1111111_opy_.bstack1llllll11_opy_(bs_config),
    bstack1111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ▁"): bs_config.get(bstack1111_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ▂"), False),
    bstack1111_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ▃"): bstack1111lll1ll_opy_,
    bstack1111_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭▄"): bstack11111ll11_opy_,
    bstack1111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ▅"): bstack1ll1ll1l1l11_opy_
  }
  return bstack1ll11ll1_opy_
@error_handler(class_method=False)
def bstack1ll1lll1111l_opy_(bs_config):
  try:
    bstack1ll1ll1lllll_opy_ = json.loads(os.getenv(bstack1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ▆"), bstack1111_opy_ (u"ࠪࡿࢂ࠭▇")))
    bstack1ll1ll1lllll_opy_ = bstack1ll1ll1ll111_opy_(bs_config, bstack1ll1ll1lllll_opy_)
    return {
        bstack1111_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭█"): bstack1ll1ll1lllll_opy_
    }
  except Exception as error:
    logger.error(bstack1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡪࡩࡹࡥࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡥࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦ▉").format(str(error)))
    return {}
def bstack1ll1ll1ll111_opy_(bs_config, bstack1ll1ll1lllll_opy_):
  if ((bstack1111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ▊") in bs_config or not bstack1ll11ll11l_opy_(bs_config)) and bstack11l1111111_opy_.bstack1llllll11_opy_(bs_config)):
    bstack1ll1ll1lllll_opy_[bstack1111_opy_ (u"ࠢࡪࡰࡦࡰࡺࡪࡥࡆࡰࡦࡳࡩ࡫ࡤࡆࡺࡷࡩࡳࡹࡩࡰࡰࠥ▋")] = True
  return bstack1ll1ll1lllll_opy_
def bstack1ll1lll11ll1_opy_(array, bstack1ll1ll1ll1ll_opy_, bstack1ll1ll1ll1l1_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1ll1ll1ll_opy_]
    result[key] = o[bstack1ll1ll1ll1l1_opy_]
  return result
def bstack1ll1lll1ll11_opy_(bstack111ll11ll_opy_=bstack1111_opy_ (u"ࠨࠩ▌")):
  bstack1ll1ll1lll11_opy_ = bstack11l1111111_opy_.on()
  bstack1ll1ll1lll1l_opy_ = bstack11l111ll11_opy_.on()
  bstack1ll1ll1l1l1l_opy_ = percy.bstack1lll1l1l_opy_()
  if bstack1ll1ll1l1l1l_opy_ and not bstack1ll1ll1lll1l_opy_ and not bstack1ll1ll1lll11_opy_:
    return bstack111ll11ll_opy_ not in [bstack1111_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭▍"), bstack1111_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ▎")]
  elif bstack1ll1ll1lll11_opy_ and not bstack1ll1ll1lll1l_opy_:
    return bstack111ll11ll_opy_ not in [bstack1111_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬ▏"), bstack1111_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ▐"), bstack1111_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ░")]
  return bstack1ll1ll1lll11_opy_ or bstack1ll1ll1lll1l_opy_ or bstack1ll1ll1l1l1l_opy_
@error_handler(class_method=False)
def bstack1ll1lll111l1_opy_(bstack111ll11ll_opy_, test=None):
  bstack1ll1ll1l1ll1_opy_ = bstack11l1111111_opy_.on()
  if not bstack1ll1ll1l1ll1_opy_ or bstack111ll11ll_opy_ not in [bstack1111_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ▒")] or test == None:
    return None
  return {
    bstack1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ▓"): bstack1ll1ll1l1ll1_opy_ and bstack1lll11lll1_opy_(threading.current_thread(), bstack1111_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ▔"), None) == True and bstack11l1111111_opy_.bstack111l1lll1_opy_(test[bstack1111_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ▕")])
  }
def bstack1ll1ll1l1lll_opy_(bs_config, framework):
  bstack11111ll11_opy_ = False
  bstack1111lll1ll_opy_ = False
  bstack1ll1ll1l1l11_opy_ = False
  if bstack1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ▖") in bs_config:
    bstack1ll1ll1l1l11_opy_ = True
  elif bstack1111_opy_ (u"ࠬࡧࡰࡱࠩ▗") in bs_config:
    bstack11111ll11_opy_ = True
  else:
    bstack1111lll1ll_opy_ = True
  bstack1ll11ll1_opy_ = {
    bstack1111_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭▘"): bstack11l111ll11_opy_.bstack1ll1ll1llll1_opy_(bs_config, framework),
    bstack1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ▙"): bstack11l1111111_opy_.bstack1l1l1ll1l_opy_(bs_config),
    bstack1111_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ▚"): bs_config.get(bstack1111_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ▛"), False),
    bstack1111_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ▜"): bstack1111lll1ll_opy_,
    bstack1111_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ▝"): bstack11111ll11_opy_,
    bstack1111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ▞"): bstack1ll1ll1l1l11_opy_
  }
  return bstack1ll11ll1_opy_