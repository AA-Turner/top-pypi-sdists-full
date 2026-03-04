# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack111l111_opy_ = 2048
bstack1l111l1_opy_ = 7
def bstack1lll1l_opy_ (bstack1l1l11_opy_):
    global bstack1lll1ll_opy_
    bstack1ll111l_opy_ = ord (bstack1l1l11_opy_ [-1])
    bstack1lll_opy_ = bstack1l1l11_opy_ [:-1]
    bstack11ll1_opy_ = bstack1ll111l_opy_ % len (bstack1lll_opy_)
    bstack11l11l1_opy_ = bstack1lll_opy_ [:bstack11ll1_opy_] + bstack1lll_opy_ [bstack11ll1_opy_:]
    if bstack1lll1l1_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack111l111_opy_ - (bstack1l11111_opy_ + bstack1ll111l_opy_) % bstack1l111l1_opy_) for bstack1l11111_opy_, char in enumerate (bstack11l11l1_opy_)])
    return eval (bstack111l11_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11l111l1111_opy_, bstack1ll1111l1l_opy_, get_host_info, bstack1111lll1lll_opy_, \
 bstack11lll11l1l_opy_, bstack1lll111ll_opy_, error_handler, bstack1111ll1l11l_opy_, current_time
import bstack_utils.accessibility as bstack11l1111111_opy_
from bstack_utils.bstack1lll1ll111_opy_ import bstack11l1llll1_opy_
from bstack_utils.bstack1111ll1111_opy_ import bstack111lllll1_opy_
from bstack_utils.percy import bstack1l1l1l1l_opy_
from bstack_utils.config import Config
global_config = Config.get_instance()
logger = logging.getLogger(__name__)
percy = bstack1l1l1l1l_opy_()
@error_handler(class_method=False)
def bstack1ll1llll1111_opy_(bs_config, bstack11l1l1l1_opy_):
  try:
    data = {
        bstack1lll1l_opy_ (u"ࠧࡧࡱࡵࡱࡦࡺࠧ╓"): bstack1lll1l_opy_ (u"ࠨ࡬ࡶࡳࡳ࠭╔"),
        bstack1lll1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡢࡲࡦࡳࡥࠨ╕"): bs_config.get(bstack1lll1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ╖"), bstack1lll1l_opy_ (u"ࠫࠬ╗")),
        bstack1lll1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ╘"): bs_config.get(bstack1lll1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ╙"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1lll1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ╚"): bs_config.get(bstack1lll1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ╛")),
        bstack1lll1l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ╜"): bs_config.get(bstack1lll1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭╝"), bstack1lll1l_opy_ (u"ࠫࠬ╞")),
        bstack1lll1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ╟"): current_time(),
        bstack1lll1l_opy_ (u"࠭ࡴࡢࡩࡶࠫ╠"): bstack1111lll1lll_opy_(bs_config),
        bstack1lll1l_opy_ (u"ࠧࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠪ╡"): get_host_info(),
        bstack1lll1l_opy_ (u"ࠨࡥ࡬ࡣ࡮ࡴࡦࡰࠩ╢"): bstack1ll1111l1l_opy_(),
        bstack1lll1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡴࡸࡲࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ╣"): os.environ.get(bstack1lll1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ╤")),
        bstack1lll1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡸࡵ࡯ࠩ╥"): os.environ.get(bstack1lll1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪ╦"), False),
        bstack1lll1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡤࡱࡱࡸࡷࡵ࡬ࠨ╧"): bstack11l111l1111_opy_(),
        bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ╨"): bstack1ll1ll1ll1ll_opy_(bs_config),
        bstack1lll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠬ╩"): bstack1ll1ll1ll11l_opy_(bstack11l1l1l1_opy_),
        bstack1lll1l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ╪"): bstack1ll1ll1lllll_opy_(bs_config, bstack11l1l1l1_opy_.get(bstack1lll1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫ╫"), bstack1lll1l_opy_ (u"ࠫࠬ╬"))),
        bstack1lll1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ╭"): bstack11lll11l1l_opy_(bs_config),
        bstack1lll1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠫ╮"): bstack1ll1ll1ll111_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1lll1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ╯").format(str(error)))
    return None
def bstack1ll1ll1ll11l_opy_(framework):
  return {
    bstack1lll1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ╰"): framework.get(bstack1lll1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ╱"), bstack1lll1l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ╲")),
    bstack1lll1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ╳"): framework.get(bstack1lll1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ╴")),
    bstack1lll1l_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ╵"): framework.get(bstack1lll1l_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ╶")),
    bstack1lll1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ╷"): bstack1lll1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ╸"),
    bstack1lll1l_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ╹"): framework.get(bstack1lll1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ╺"))
  }
def bstack1ll1ll1ll111_opy_(bs_config):
  bstack1lll1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡴࡶࡤࡶࡹ࠴ࠊࠡࠢࠥࠦࠧ╻")
  if not bs_config:
    return {}
  bstack1llll1lllll1_opy_ = bstack11l1llll1_opy_(bs_config).bstack1lllll1l1lll_opy_(bs_config)
  return bstack1llll1lllll1_opy_
def bstack11lllllll1_opy_(bs_config, framework):
  bstack1ll11l1l_opy_ = False
  bstack1l11l11ll_opy_ = False
  bstack1ll1ll1l1lll_opy_ = False
  if bstack1lll1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ╼") in bs_config:
    bstack1ll1ll1l1lll_opy_ = True
  elif bstack1lll1l_opy_ (u"ࠧࡢࡲࡳࠫ╽") in bs_config:
    bstack1ll11l1l_opy_ = True
  else:
    bstack1l11l11ll_opy_ = True
  bstack11ll111l11_opy_ = {
    bstack1lll1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ╾"): bstack111lllll1_opy_.bstack1ll1ll1llll1_opy_(bs_config, framework),
    bstack1lll1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ╿"): bstack11l1111111_opy_.bstack1l11ll11l1_opy_(bs_config),
    bstack1lll1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ▀"): bs_config.get(bstack1lll1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ▁"), False),
    bstack1lll1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ▂"): bstack1l11l11ll_opy_,
    bstack1lll1l_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ▃"): bstack1ll11l1l_opy_,
    bstack1lll1l_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ▄"): bstack1ll1ll1l1lll_opy_
  }
  return bstack11ll111l11_opy_
@error_handler(class_method=False)
def bstack1ll1ll1ll1ll_opy_(bs_config):
  try:
    bstack1ll1ll1ll1l1_opy_ = json.loads(os.getenv(bstack1lll1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ▅"), bstack1lll1l_opy_ (u"ࠩࡾࢁࠬ▆")))
    bstack1ll1ll1ll1l1_opy_ = bstack1ll1lll111l1_opy_(bs_config, bstack1ll1ll1ll1l1_opy_)
    return {
        bstack1lll1l_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬ▇"): bstack1ll1ll1ll1l1_opy_
    }
  except Exception as error:
    logger.error(bstack1lll1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥ█").format(str(error)))
    return {}
def bstack1ll1lll111l1_opy_(bs_config, bstack1ll1ll1ll1l1_opy_):
  if ((bstack1lll1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ▉") in bs_config or not bstack11lll11l1l_opy_(bs_config)) and bstack11l1111111_opy_.bstack1l11ll11l1_opy_(bs_config)):
    bstack1ll1ll1ll1l1_opy_[bstack1lll1l_opy_ (u"ࠨࡩ࡯ࡥ࡯ࡹࡩ࡫ࡅ࡯ࡥࡲࡨࡪࡪࡅࡹࡶࡨࡲࡸ࡯࡯࡯ࠤ▊")] = True
  return bstack1ll1ll1ll1l1_opy_
def bstack1ll1lll11ll1_opy_(array, bstack1ll1lll1111l_opy_, bstack1ll1ll1l1ll1_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1lll1111l_opy_]
    result[key] = o[bstack1ll1ll1l1ll1_opy_]
  return result
def bstack1ll1lll11l1l_opy_(bstack11l111l11_opy_=bstack1lll1l_opy_ (u"ࠧࠨ▋")):
  bstack1ll1lll111ll_opy_ = bstack11l1111111_opy_.on()
  bstack1ll1ll1lll11_opy_ = bstack111lllll1_opy_.on()
  bstack1ll1ll1lll1l_opy_ = percy.bstack11l1ll1lll_opy_()
  if bstack1ll1ll1lll1l_opy_ and not bstack1ll1ll1lll11_opy_ and not bstack1ll1lll111ll_opy_:
    return bstack11l111l11_opy_ not in [bstack1lll1l_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬ▌"), bstack1lll1l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭▍")]
  elif bstack1ll1lll111ll_opy_ and not bstack1ll1ll1lll11_opy_:
    return bstack11l111l11_opy_ not in [bstack1lll1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ▎"), bstack1lll1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭▏"), bstack1lll1l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ▐")]
  return bstack1ll1lll111ll_opy_ or bstack1ll1ll1lll11_opy_ or bstack1ll1ll1lll1l_opy_
@error_handler(class_method=False)
def bstack1ll1llll11ll_opy_(bstack11l111l11_opy_, test=None):
  bstack1ll1lll11111_opy_ = bstack11l1111111_opy_.on()
  if not bstack1ll1lll11111_opy_ or bstack11l111l11_opy_ not in [bstack1lll1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ░")] or test == None:
    return None
  return {
    bstack1lll1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ▒"): bstack1ll1lll11111_opy_ and bstack1lll111ll_opy_(threading.current_thread(), bstack1lll1l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ▓"), None) == True and bstack11l1111111_opy_.bstack1lll11ll_opy_(test[bstack1lll1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ▔")])
  }
def bstack1ll1ll1lllll_opy_(bs_config, framework):
  bstack1ll11l1l_opy_ = False
  bstack1l11l11ll_opy_ = False
  bstack1ll1ll1l1lll_opy_ = False
  if bstack1lll1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ▕") in bs_config:
    bstack1ll1ll1l1lll_opy_ = True
  elif bstack1lll1l_opy_ (u"ࠫࡦࡶࡰࠨ▖") in bs_config:
    bstack1ll11l1l_opy_ = True
  else:
    bstack1l11l11ll_opy_ = True
  bstack11ll111l11_opy_ = {
    bstack1lll1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ▗"): bstack111lllll1_opy_.bstack1ll1ll1llll1_opy_(bs_config, framework),
    bstack1lll1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭▘"): bstack11l1111111_opy_.bstack11111111_opy_(bs_config),
    bstack1lll1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭▙"): bs_config.get(bstack1lll1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ▚"), False),
    bstack1lll1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ▛"): bstack1l11l11ll_opy_,
    bstack1lll1l_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ▜"): bstack1ll11l1l_opy_,
    bstack1lll1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ▝"): bstack1ll1ll1l1lll_opy_
  }
  return bstack11ll111l11_opy_