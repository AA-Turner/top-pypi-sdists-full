# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111llll11ll_opy_, bstack11llll111_opy_, get_host_info, bstack11111llllll_opy_, \
 bstack11l1ll11ll_opy_, bstack1l11l11l11_opy_, error_handler, bstack1111l111l11_opy_, current_time
import bstack_utils.accessibility as a11y
from bstack_utils.bstack11llllll1_opy_ import bstack11ll11l11l_opy_
from bstack_utils.bstack1lll1lll_opy_ import bstack11l11ll1l1_opy_
from bstack_utils.percy import bstack1llll111ll_opy_
from bstack_utils.config import Config
global_config = Config.get_instance()
logger = logging.getLogger(__name__)
percy = bstack1llll111ll_opy_()
@error_handler(class_method=False)
def bstack1ll1lll11111_opy_(bs_config, bstack1ll111l111_opy_):
  try:
    data = {
        bstack1111l_opy_ (u"ࠪࡪࡴࡸ࡭ࡢࡶࠪ☚"): bstack1111l_opy_ (u"ࠫ࡯ࡹ࡯࡯ࠩ☛"),
        bstack1111l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡥ࡮ࡢ࡯ࡨࠫ☜"): bs_config.get(bstack1111l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ☝"), bstack1111l_opy_ (u"ࠧࠨ☞")),
        bstack1111l_opy_ (u"ࠨࡰࡤࡱࡪ࠭☟"): bs_config.get(bstack1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ☠"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭☡"): bs_config.get(bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭☢")),
        bstack1111l_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ☣"): bs_config.get(bstack1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ☤"), bstack1111l_opy_ (u"ࠧࠨ☥")),
        bstack1111l_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ☦"): current_time(),
        bstack1111l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ☧"): bstack11111llllll_opy_(bs_config),
        bstack1111l_opy_ (u"ࠪ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴ࠭☨"): get_host_info(),
        bstack1111l_opy_ (u"ࠫࡨ࡯࡟ࡪࡰࡩࡳࠬ☩"): bstack11llll111_opy_(),
        bstack1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡷࡻ࡮ࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ☪"): os.environ.get(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ☫")),
        bstack1111l_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡴࡸࡲࠬ☬"): os.environ.get(bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭☭"), False),
        bstack1111l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡢࡧࡴࡴࡴࡳࡱ࡯ࠫ☮"): bstack111llll11ll_opy_(),
        bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ☯"): bstack1ll1ll1111l1_opy_(bs_config),
        bstack1111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠨ☰"): bstack1ll1ll11l111_opy_(bstack1ll111l111_opy_),
        bstack1111l_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪ☱"): bstack1ll1ll11ll11_opy_(bs_config, bstack1ll111l111_opy_.get(bstack1111l_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧ☲"), bstack1111l_opy_ (u"ࠧࠨ☳"))),
        bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ☴"): bstack11l1ll11ll_opy_(bs_config),
        bstack1111l_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠧ☵"): bstack1ll1ll11l11l_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦ☶").format(str(error)))
    return None
def bstack1ll1ll11l111_opy_(framework):
  return {
    bstack1111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫ☷"): framework.get(bstack1111l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭☸"), bstack1111l_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭☹")),
    bstack1111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ☺"): framework.get(bstack1111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ☻")),
    bstack1111l_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭☼"): framework.get(bstack1111l_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ☽")),
    bstack1111l_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭☾"): bstack1111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ☿"),
    bstack1111l_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭♀"): framework.get(bstack1111l_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ♁"))
  }
def bstack1ll1ll11l11l_opy_(bs_config):
  bstack1111l_opy_ (u"ࠣࠤࠥࠎࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡧࡻࡩ࡭ࡦࠣࡷࡹࡧࡲࡵ࠰ࠍࠤࠥࠨࠢࠣ♂")
  if not bs_config:
    return {}
  bstack1llll1l11lll_opy_ = bstack11ll11l11l_opy_(bs_config).bstack1llll1l1111l_opy_(bs_config)
  return bstack1llll1l11lll_opy_
def bstack11l11l1111_opy_(bs_config, framework):
  bstack1ll1111111_opy_ = False
  bstack111llllll1_opy_ = False
  bstack1ll1ll1111ll_opy_ = False
  if bstack1111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭♃") in bs_config:
    bstack1ll1ll1111ll_opy_ = True
  elif bstack1111l_opy_ (u"ࠪࡥࡵࡶࠧ♄") in bs_config:
    bstack1ll1111111_opy_ = True
  else:
    bstack111llllll1_opy_ = True
  bstack11llll11_opy_ = {
    bstack1111l_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ♅"): bstack11l11ll1l1_opy_.bstack1ll1ll11l1ll_opy_(bs_config, framework),
    bstack1111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ♆"): a11y.is_enabled_root(bs_config),
    bstack1111l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ♇"): bs_config.get(bstack1111l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭♈"), False),
    bstack1111l_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ♉"): bstack111llllll1_opy_,
    bstack1111l_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ♊"): bstack1ll1111111_opy_,
    bstack1111l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ♋"): bstack1ll1ll1111ll_opy_
  }
  return bstack11llll11_opy_
@error_handler(class_method=False)
def bstack1ll1ll1111l1_opy_(bs_config):
  try:
    bstack1ll1ll111l1l_opy_ = json.loads(os.getenv(bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ♌"), bstack1111l_opy_ (u"ࠬࢁࡽࠨ♍")))
    bstack1ll1ll111l1l_opy_ = bstack1ll1ll111lll_opy_(bs_config, bstack1ll1ll111l1l_opy_)
    return {
        bstack1111l_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨ♎"): bstack1ll1ll111l1l_opy_
    }
  except Exception as error:
    logger.error(bstack1111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨ♏").format(str(error)))
    return {}
def bstack1ll1ll111lll_opy_(bs_config, bstack1ll1ll111l1l_opy_):
  if ((bstack1111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ♐") in bs_config or not bstack11l1ll11ll_opy_(bs_config)) and a11y.is_enabled_root(bs_config)):
    bstack1ll1ll111l1l_opy_[bstack1111l_opy_ (u"ࠤ࡬ࡲࡨࡲࡵࡥࡧࡈࡲࡨࡵࡤࡦࡦࡈࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠧ♑")] = True
  return bstack1ll1ll111l1l_opy_
def bstack1ll1ll1ll11l_opy_(array, bstack1ll1ll111ll1_opy_, bstack1ll1ll11l1l1_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1ll111ll1_opy_]
    result[key] = o[bstack1ll1ll11l1l1_opy_]
  return result
def bstack1ll1ll11llll_opy_(bstack111lll11l_opy_=bstack1111l_opy_ (u"ࠪࠫ♒")):
  bstack1ll1ll111l11_opy_ = a11y.on()
  bstack1ll1ll11111l_opy_ = bstack11l11ll1l1_opy_.on()
  bstack1ll1ll11lll1_opy_ = percy.bstack1l11111l1l_opy_()
  if bstack1ll1ll11lll1_opy_ and not bstack1ll1ll11111l_opy_ and not bstack1ll1ll111l11_opy_:
    return bstack111lll11l_opy_ not in [bstack1111l_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨ♓"), bstack1111l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ♔")]
  elif bstack1ll1ll111l11_opy_ and not bstack1ll1ll11111l_opy_:
    return bstack111lll11l_opy_ not in [bstack1111l_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ♕"), bstack1111l_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ♖"), bstack1111l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ♗")]
  return bstack1ll1ll111l11_opy_ or bstack1ll1ll11111l_opy_ or bstack1ll1ll11lll1_opy_
@error_handler(class_method=False)
def bstack1ll1ll1ll1ll_opy_(bstack111lll11l_opy_, test=None):
  bstack1ll1ll11ll1l_opy_ = a11y.on()
  if not bstack1ll1ll11ll1l_opy_ or bstack111lll11l_opy_ not in [bstack1111l_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ♘"), bstack1111l_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ♙"), bstack1111l_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨ♚")] or test == None:
    return None
  return {
    bstack1111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ♛"): bstack1ll1ll11ll1l_opy_ and bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ♜"), None) == True and a11y.is_enabled_testcase(test.get(bstack1111l_opy_ (u"ࠧࡵࡣࡪࡷࠬ♝"), []))
  }
def bstack1ll1ll11ll11_opy_(bs_config, framework):
  bstack1ll1111111_opy_ = False
  bstack111llllll1_opy_ = False
  bstack1ll1ll1111ll_opy_ = False
  if bstack1111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ♞") in bs_config:
    bstack1ll1ll1111ll_opy_ = True
  elif bstack1111l_opy_ (u"ࠩࡤࡴࡵ࠭♟") in bs_config:
    bstack1ll1111111_opy_ = True
  else:
    bstack111llllll1_opy_ = True
  bstack11llll11_opy_ = {
    bstack1111l_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ♠"): bstack11l11ll1l1_opy_.bstack1ll1ll11l1ll_opy_(bs_config, framework),
    bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ♡"): a11y.bstack1l1l1l1ll1_opy_(bs_config),
    bstack1111l_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ♢"): bs_config.get(bstack1111l_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ♣"), False),
    bstack1111l_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ♤"): bstack111llllll1_opy_,
    bstack1111l_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ♥"): bstack1ll1111111_opy_,
    bstack1111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭♦"): bstack1ll1ll1111ll_opy_
  }
  return bstack11llll11_opy_