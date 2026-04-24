# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack1111l1lllll_opy_, bstack1l11111lll_opy_, get_host_info, bstack1llll111l111_opy_, \
 bstack11lll11l11_opy_, bstack111lll1ll1_opy_, error_handler, bstack1llll1ll111l_opy_, bstack1llllll1l11_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.bstack111l11lll_opy_ import bstack1l1111ll11_opy_
from bstack_utils.bstack11lll111_opy_ import bstack1lll1l11l_opy_
from bstack_utils.percy import bstack1llll1l11l_opy_
from bstack_utils.config import Config
global_config = Config.bstack1lllll1lll1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1llll1l11l_opy_()
@error_handler(class_method=False)
def bstack1ll111ll111l_opy_(bs_config, bstack111ll1111l_opy_):
  try:
    data = {
        bstack111ll11_opy_ (u"ࠫ࡫ࡵࡲ࡮ࡣࡷࠫ⢭"): bstack111ll11_opy_ (u"ࠬࡰࡳࡰࡰࠪ⢮"),
        bstack111ll11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺ࡟࡯ࡣࡰࡩࠬ⢯"): bs_config.get(bstack111ll11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ⢰"), bstack111ll11_opy_ (u"ࠨࠩ⢱")),
        bstack111ll11_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ⢲"): bs_config.get(bstack111ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭⢳"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack111ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⢴"): bs_config.get(bstack111ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⢵")),
        bstack111ll11_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ⢶"): bs_config.get(bstack111ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ⢷"), bstack111ll11_opy_ (u"ࠨࠩ⢸")),
        bstack111ll11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡦࡦࡢࡥࡹ࠭⢹"): bstack1llllll1l11_opy_(),
        bstack111ll11_opy_ (u"ࠪࡸࡦ࡭ࡳࠨ⢺"): bstack1llll111l111_opy_(bs_config),
        bstack111ll11_opy_ (u"ࠫ࡭ࡵࡳࡵࡡ࡬ࡲ࡫ࡵࠧ⢻"): get_host_info(),
        bstack111ll11_opy_ (u"ࠬࡩࡩࡠ࡫ࡱࡪࡴ࠭⢼"): bstack1l11111lll_opy_(),
        bstack111ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡸࡵ࡯ࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭⢽"): os.environ.get(bstack111ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡂࡖࡋࡏࡈࡤࡘࡕࡏࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭⢾")),
        bstack111ll11_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࡠࡶࡨࡷࡹࡹ࡟ࡳࡧࡵࡹࡳ࠭⢿"): os.environ.get(bstack111ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡔࡈࡖ࡚ࡔࠧ⣀"), False),
        bstack111ll11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡣࡨࡵ࡮ࡵࡴࡲࡰࠬ⣁"): bstack1111l1lllll_opy_(),
        bstack111ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⣂"): bstack1ll111l111l1_opy_(bs_config),
        bstack111ll11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡦࡨࡸࡦ࡯࡬ࡴࠩ⣃"): bstack1ll111l11l11_opy_(bstack111ll1111l_opy_),
        bstack111ll11_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫ⣄"): bstack1ll111l11l1l_opy_(bs_config, bstack111ll1111l_opy_.get(bstack111ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨ⣅"), bstack111ll11_opy_ (u"ࠨࠩ⣆"))),
        bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ⣇"): bstack11lll11l11_opy_(bs_config),
        bstack111ll11_opy_ (u"ࠪࡸࡪࡹࡴࡠࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠨ⣈"): bstack1ll111l1ll11_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack111ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡤࡽࡱࡵࡡࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ⣉").format(str(error)))
    return None
def bstack1ll111l11l11_opy_(framework):
  return {
    bstack111ll11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬ⣊"): framework.get(bstack111ll11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧ⣋"), bstack111ll11_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧ⣌")),
    bstack111ll11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ⣍"): framework.get(bstack111ll11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⣎")),
    bstack111ll11_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ⣏"): framework.get(bstack111ll11_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⣐")),
    bstack111ll11_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧ⣑"): bstack111ll11_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭⣒"),
    bstack111ll11_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⣓"): framework.get(bstack111ll11_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⣔"))
  }
def bstack1ll111l1ll11_opy_(bs_config):
  bstack111ll11_opy_ (u"ࠤࠥࠦࠏࠦࠠࡓࡧࡷࡹࡷࡴࡳࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠣࡨࡦࡺࡡࠡࡨࡲࡶࠥࡨࡵࡪ࡮ࡧࠤࡸࡺࡡࡳࡶ࠱ࠎࠥࠦࠢࠣࠤ⣕")
  if not bs_config:
    return {}
  bstack1lll11ll1111_opy_ = bstack1l1111ll11_opy_(bs_config).bstack1ll1lllll1l1_opy_(bs_config)
  return bstack1lll11ll1111_opy_
def bstack1l1ll1l11l_opy_(bs_config, framework):
  bstack11l11l111l_opy_ = False
  bstack1l1lll1l11_opy_ = False
  bstack1ll111l1l11l_opy_ = False
  if bstack111ll11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⣖") in bs_config:
    bstack1ll111l1l11l_opy_ = True
  elif bstack111ll11_opy_ (u"ࠫࡦࡶࡰࠨ⣗") in bs_config:
    bstack11l11l111l_opy_ = True
  else:
    bstack1l1lll1l11_opy_ = True
  bstack11l11l11ll_opy_ = {
    bstack111ll11_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⣘"): bstack1lll1l11l_opy_.bstack1ll111l11111_opy_(bs_config, framework),
    bstack111ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⣙"): a11y.is_enabled_root(bs_config),
    bstack111ll11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⣚"): bs_config.get(bstack111ll11_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⣛"), False),
    bstack111ll11_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⣜"): bstack1l1lll1l11_opy_,
    bstack111ll11_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ⣝"): bstack11l11l111l_opy_,
    bstack111ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⣞"): bstack1ll111l1l11l_opy_
  }
  return bstack11l11l11ll_opy_
@error_handler(class_method=False)
def bstack1ll111l111l1_opy_(bs_config):
  try:
    bstack1ll111l1l1ll_opy_ = json.loads(os.getenv(bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭⣟"), bstack111ll11_opy_ (u"࠭ࡻࡾࠩ⣠")))
    bstack1ll111l1l1ll_opy_ = bstack1ll111l1l111_opy_(bs_config, bstack1ll111l1l1ll_opy_)
    return {
        bstack111ll11_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩ⣡"): bstack1ll111l1l1ll_opy_
    }
  except Exception as error:
    logger.error(bstack111ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢ⣢").format(str(error)))
    return {}
def bstack1ll111l1l111_opy_(bs_config, bstack1ll111l1l1ll_opy_):
  if ((bstack111ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⣣") in bs_config or not bstack11lll11l11_opy_(bs_config)) and a11y.is_enabled_root(bs_config)):
    bstack1ll111l1l1ll_opy_[bstack111ll11_opy_ (u"ࠥ࡭ࡳࡩ࡬ࡶࡦࡨࡉࡳࡩ࡯ࡥࡧࡧࡉࡽࡺࡥ࡯ࡵ࡬ࡳࡳࠨ⣤")] = True
  return bstack1ll111l1l1ll_opy_
def bstack1ll111lll1l1_opy_(array, bstack1ll111l1l1l1_opy_, bstack1ll111l11ll1_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll111l1l1l1_opy_]
    result[key] = o[bstack1ll111l11ll1_opy_]
  return result
def bstack1ll11l1111l1_opy_(bstack11l111l11_opy_=bstack111ll11_opy_ (u"ࠫࠬ⣥")):
  bstack1ll111l111ll_opy_ = a11y.on()
  bstack1ll111l1ll1l_opy_ = bstack1lll1l11l_opy_.on()
  bstack1ll111l1111l_opy_ = percy.bstack1llll11lll_opy_()
  if bstack1ll111l1111l_opy_ and not bstack1ll111l1ll1l_opy_ and not bstack1ll111l111ll_opy_:
    return bstack11l111l11_opy_ not in [bstack111ll11_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩ⣦"), bstack111ll11_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ⣧")]
  elif bstack1ll111l111ll_opy_ and not bstack1ll111l1ll1l_opy_:
    return bstack11l111l11_opy_ not in [bstack111ll11_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⣨"), bstack111ll11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⣩"), bstack111ll11_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭⣪")]
  return bstack1ll111l111ll_opy_ or bstack1ll111l1ll1l_opy_ or bstack1ll111l1111l_opy_
@error_handler(class_method=False)
def bstack1ll11l111111_opy_(bstack11l111l11_opy_, test=None):
  bstack1ll111l11lll_opy_ = a11y.on()
  if not bstack1ll111l11lll_opy_ or bstack11l111l11_opy_ not in [bstack111ll11_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⣫"), bstack111ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⣬"), bstack111ll11_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩ⣭")] or test == None:
    return None
  return {
    bstack111ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⣮"): bstack1ll111l11lll_opy_ and bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⣯"), None) == True and a11y.is_enabled_testcase(test.get(bstack111ll11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭⣰"), []))
  }
def bstack1ll111l11l1l_opy_(bs_config, framework):
  bstack11l11l111l_opy_ = False
  bstack1l1lll1l11_opy_ = False
  bstack1ll111l1l11l_opy_ = False
  if bstack111ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⣱") in bs_config:
    bstack1ll111l1l11l_opy_ = True
  elif bstack111ll11_opy_ (u"ࠪࡥࡵࡶࠧ⣲") in bs_config:
    bstack11l11l111l_opy_ = True
  else:
    bstack1l1lll1l11_opy_ = True
  bstack11l11l11ll_opy_ = {
    bstack111ll11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⣳"): bstack1lll1l11l_opy_.bstack1ll111l11111_opy_(bs_config, framework),
    bstack111ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⣴"): a11y.bstack11111ll11_opy_(bs_config),
    bstack111ll11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⣵"): bs_config.get(bstack111ll11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⣶"), False),
    bstack111ll11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⣷"): bstack1l1lll1l11_opy_,
    bstack111ll11_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ⣸"): bstack11l11l111l_opy_,
    bstack111ll11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ⣹"): bstack1ll111l1l11l_opy_
  }
  return bstack11l11l11ll_opy_