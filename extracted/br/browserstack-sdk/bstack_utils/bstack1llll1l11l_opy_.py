# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack1111l1l1lll_opy_, bstack1ll1lll1ll_opy_, get_host_info, bstack1llll11ll1l1_opy_, \
 bstack11lllllll_opy_, bstack11l11l11_opy_, error_handler, bstack1lllll1l111l_opy_, bstack1l111l1ll_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.bstack11lll1lll_opy_ import bstack1lll1111ll_opy_
from bstack_utils.bstack11l1l111l_opy_ import bstack1l1lll1l1_opy_
from bstack_utils.percy import bstack11l111llll_opy_
from bstack_utils.config import Config
global_config = Config.bstack111111l1ll_opy_()
logger = logging.getLogger(__name__)
percy = bstack11l111llll_opy_()
@error_handler(class_method=False)
def bstack1ll111ll1lll_opy_(bs_config, bstack11ll111l11_opy_):
  try:
    data = {
        bstack1l1111l_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭⢯"): bstack1l1111l_opy_ (u"ࠧ࡫ࡵࡲࡲࠬ⢰"),
        bstack1l1111l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧ⢱"): bs_config.get(bstack1l1111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ⢲"), bstack1l1111l_opy_ (u"ࠪࠫ⢳")),
        bstack1l1111l_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⢴"): bs_config.get(bstack1l1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ⢵"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1111l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⢶"): bs_config.get(bstack1l1111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⢷")),
        bstack1l1111l_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭⢸"): bs_config.get(bstack1l1111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ⢹"), bstack1l1111l_opy_ (u"ࠪࠫ⢺")),
        bstack1l1111l_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⢻"): bstack1l111l1ll_opy_(),
        bstack1l1111l_opy_ (u"ࠬࡺࡡࡨࡵࠪ⢼"): bstack1llll11ll1l1_opy_(bs_config),
        bstack1l1111l_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩ⢽"): get_host_info(),
        bstack1l1111l_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨ⢾"): bstack1ll1lll1ll_opy_(),
        bstack1l1111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⢿"): os.environ.get(bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ⣀")),
        bstack1l1111l_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨ⣁"): os.environ.get(bstack1l1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩ⣂"), False),
        bstack1l1111l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧ⣃"): bstack1111l1l1lll_opy_(),
        bstack1l1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⣄"): bstack1ll1111lllll_opy_(bs_config),
        bstack1l1111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡨࡪࡺࡡࡪ࡮ࡶࠫ⣅"): bstack1ll111l11l11_opy_(bstack11ll111l11_opy_),
        bstack1l1111l_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭⣆"): bstack1ll1111llll1_opy_(bs_config, bstack11ll111l11_opy_.get(bstack1l1111l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ⣇"), bstack1l1111l_opy_ (u"ࠪࠫ⣈"))),
        bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⣉"): bstack11lllllll_opy_(bs_config),
        bstack1l1111l_opy_ (u"ࠬࡺࡥࡴࡶࡢࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠪ⣊"): bstack1ll111l111ll_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1l1111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢ⣋").format(str(error)))
    return None
def bstack1ll111l11l11_opy_(framework):
  return {
    bstack1l1111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧ⣌"): framework.get(bstack1l1111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩ⣍"), bstack1l1111l_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ⣎")),
    bstack1l1111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⣏"): framework.get(bstack1l1111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⣐")),
    bstack1l1111l_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ⣑"): framework.get(bstack1l1111l_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⣒")),
    bstack1l1111l_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ⣓"): bstack1l1111l_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⣔"),
    bstack1l1111l_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⣕"): framework.get(bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⣖"))
  }
def bstack1ll111l111ll_opy_(bs_config):
  bstack1l1111l_opy_ (u"ࠦࠧࠨࠊࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡳࡵࡣࡵࡸ࠳ࠐࠠࠡࠤࠥࠦ⣗")
  if not bs_config:
    return {}
  bstack1lll11111lll_opy_ = bstack1lll1111ll_opy_(bs_config).bstack1ll1llll1ll1_opy_(bs_config)
  return bstack1lll11111lll_opy_
def bstack111111llll_opy_(bs_config, framework):
  bstack1111l111l_opy_ = False
  bstack1ll11l1l11_opy_ = False
  bstack1ll111l1l1l1_opy_ = False
  if bstack1l1111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⣘") in bs_config:
    bstack1ll111l1l1l1_opy_ = True
  elif bstack1l1111l_opy_ (u"࠭ࡡࡱࡲࠪ⣙") in bs_config:
    bstack1111l111l_opy_ = True
  else:
    bstack1ll11l1l11_opy_ = True
  bstack1ll1lll11l_opy_ = {
    bstack1l1111l_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⣚"): bstack1l1lll1l1_opy_.bstack1ll111l111l1_opy_(bs_config, framework),
    bstack1l1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⣛"): a11y.is_enabled_root(bs_config),
    bstack1l1111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⣜"): bs_config.get(bstack1l1111l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⣝"), False),
    bstack1l1111l_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⣞"): bstack1ll11l1l11_opy_,
    bstack1l1111l_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⣟"): bstack1111l111l_opy_,
    bstack1l1111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ⣠"): bstack1ll111l1l1l1_opy_
  }
  return bstack1ll1lll11l_opy_
@error_handler(class_method=False)
def bstack1ll1111lllll_opy_(bs_config):
  try:
    bstack1ll111l1l11l_opy_ = json.loads(os.getenv(bstack1l1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ⣡"), bstack1l1111l_opy_ (u"ࠨࡽࢀࠫ⣢")))
    bstack1ll111l1l11l_opy_ = bstack1ll111l1l111_opy_(bs_config, bstack1ll111l1l11l_opy_)
    return {
        bstack1l1111l_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫ⣣"): bstack1ll111l1l11l_opy_
    }
  except Exception as error:
    logger.error(bstack1l1111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤ⣤").format(str(error)))
    return {}
def bstack1ll111l1l111_opy_(bs_config, bstack1ll111l1l11l_opy_):
  if ((bstack1l1111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⣥") in bs_config or not bstack11lllllll_opy_(bs_config)) and a11y.is_enabled_root(bs_config)):
    bstack1ll111l1l11l_opy_[bstack1l1111l_opy_ (u"ࠧ࡯࡮ࡤ࡮ࡸࡨࡪࡋ࡮ࡤࡱࡧࡩࡩࡋࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠣ⣦")] = True
  return bstack1ll111l1l11l_opy_
def bstack1ll111l1llll_opy_(array, bstack1ll111l11ll1_opy_, bstack1ll111l11111_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll111l11ll1_opy_]
    result[key] = o[bstack1ll111l11111_opy_]
  return result
def bstack1ll111ll1l11_opy_(bstack111l1l1l_opy_=bstack1l1111l_opy_ (u"࠭ࠧ⣧")):
  bstack1ll111l1l1ll_opy_ = a11y.on()
  bstack1ll111l1111l_opy_ = bstack1l1lll1l1_opy_.on()
  bstack1ll111l11lll_opy_ = percy.bstack111l1l1l1_opy_()
  if bstack1ll111l11lll_opy_ and not bstack1ll111l1111l_opy_ and not bstack1ll111l1l1ll_opy_:
    return bstack111l1l1l_opy_ not in [bstack1l1111l_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ⣨"), bstack1l1111l_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⣩")]
  elif bstack1ll111l1l1ll_opy_ and not bstack1ll111l1111l_opy_:
    return bstack111l1l1l_opy_ not in [bstack1l1111l_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⣪"), bstack1l1111l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⣫"), bstack1l1111l_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⣬")]
  return bstack1ll111l1l1ll_opy_ or bstack1ll111l1111l_opy_ or bstack1ll111l11lll_opy_
@error_handler(class_method=False)
def bstack1ll111llll1l_opy_(bstack111l1l1l_opy_, test=None):
  bstack1ll111l11l1l_opy_ = a11y.on()
  if not bstack1ll111l11l1l_opy_ or bstack111l1l1l_opy_ not in [bstack1l1111l_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⣭"), bstack1l1111l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⣮"), bstack1l1111l_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ⣯")] or test == None:
    return None
  return {
    bstack1l1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⣰"): bstack1ll111l11l1l_opy_ and bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ⣱"), None) == True and a11y.is_enabled_testcase(test.get(bstack1l1111l_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ⣲"), []))
  }
def bstack1ll1111llll1_opy_(bs_config, framework):
  bstack1111l111l_opy_ = False
  bstack1ll11l1l11_opy_ = False
  bstack1ll111l1l1l1_opy_ = False
  if bstack1l1111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⣳") in bs_config:
    bstack1ll111l1l1l1_opy_ = True
  elif bstack1l1111l_opy_ (u"ࠬࡧࡰࡱࠩ⣴") in bs_config:
    bstack1111l111l_opy_ = True
  else:
    bstack1ll11l1l11_opy_ = True
  bstack1ll1lll11l_opy_ = {
    bstack1l1111l_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⣵"): bstack1l1lll1l1_opy_.bstack1ll111l111l1_opy_(bs_config, framework),
    bstack1l1111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⣶"): a11y.bstack1lll11l11l_opy_(bs_config),
    bstack1l1111l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⣷"): bs_config.get(bstack1l1111l_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⣸"), False),
    bstack1l1111l_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⣹"): bstack1ll11l1l11_opy_,
    bstack1l1111l_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ⣺"): bstack1111l111l_opy_,
    bstack1l1111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ⣻"): bstack1ll111l1l1l1_opy_
  }
  return bstack1ll1lll11l_opy_