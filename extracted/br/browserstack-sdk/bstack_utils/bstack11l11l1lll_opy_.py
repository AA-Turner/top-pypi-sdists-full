# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack1111l1lll11_opy_, bstack1111l1111l_opy_, get_host_info, bstack1lllll1l111l_opy_, \
 bstack111l1lll1l_opy_, bstack11l11l1ll_opy_, error_handler, bstack1llll1l11l1l_opy_, bstack111ll1ll1l_opy_
import bstack_utils.accessibility as a11y
from bstack_utils.bstack111l1llll_opy_ import bstack11l1ll1ll_opy_
from bstack_utils.bstack111ll111ll_opy_ import bstack11l1l1l1_opy_
from bstack_utils.percy import bstack11ll111l1l_opy_
from bstack_utils.config import Config
global_config = Config.bstack1lllllll1_opy_()
logger = logging.getLogger(__name__)
percy = bstack11ll111l1l_opy_()
@error_handler(class_method=False)
def bstack1ll11l11ll11_opy_(bs_config, bstack1llll1l11_opy_):
  try:
    data = {
        bstack1ll1l11_opy_ (u"ࠩࡩࡳࡷࡳࡡࡵࠩ⡳"): bstack1ll1l11_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨ⡴"),
        bstack1ll1l11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡤࡴࡡ࡮ࡧࠪ⡵"): bs_config.get(bstack1ll1l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ⡶"), bstack1ll1l11_opy_ (u"࠭ࠧ⡷")),
        bstack1ll1l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ⡸"): bs_config.get(bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ⡹"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⡺"): bs_config.get(bstack1ll1l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ⡻")),
        bstack1ll1l11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ⡼"): bs_config.get(bstack1ll1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ⡽"), bstack1ll1l11_opy_ (u"࠭ࠧ⡾")),
        bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ⡿"): bstack111ll1ll1l_opy_(),
        bstack1ll1l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭⢀"): bstack1lllll1l111l_opy_(bs_config),
        bstack1ll1l11_opy_ (u"ࠩ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠬ⢁"): get_host_info(),
        bstack1ll1l11_opy_ (u"ࠪࡧ࡮ࡥࡩ࡯ࡨࡲࠫ⢂"): bstack1111l1111l_opy_(),
        bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡶࡺࡴ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ⢃"): os.environ.get(bstack1ll1l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ⢄")),
        bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࡸࡥࡳࡷࡱࠫ⢅"): os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬ⢆"), False),
        bstack1ll1l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡡࡦࡳࡳࡺࡲࡰ࡮ࠪ⢇"): bstack1111l1lll11_opy_(),
        bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⢈"): bstack1ll111llll11_opy_(bs_config),
        bstack1ll1l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡤࡦࡶࡤ࡭ࡱࡹࠧ⢉"): bstack1ll111ll1ll1_opy_(bstack1llll1l11_opy_),
        bstack1ll1l11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ⢊"): bstack1ll111lll1l1_opy_(bs_config, bstack1llll1l11_opy_.get(bstack1ll1l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭⢋"), bstack1ll1l11_opy_ (u"࠭ࠧ⢌"))),
        bstack1ll1l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ⢍"): bstack111l1lll1l_opy_(bs_config),
        bstack1ll1l11_opy_ (u"ࠨࡶࡨࡷࡹࡥ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠭⢎"): bstack1ll111ll1l1l_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1ll1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡢࡻ࡯ࡳࡦࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥ⢏").format(str(error)))
    return None
def bstack1ll111ll1ll1_opy_(framework):
  return {
    bstack1ll1l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪ⢐"): framework.get(bstack1ll1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬ⢑"), bstack1ll1l11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ⢒")),
    bstack1ll1l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ⢓"): framework.get(bstack1ll1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⢔")),
    bstack1ll1l11_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ⢕"): framework.get(bstack1ll1l11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⢖")),
    bstack1ll1l11_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬ⢗"): bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⢘"),
    bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⢙"): framework.get(bstack1ll1l11_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⢚"))
  }
def bstack1ll111ll1l1l_opy_(bs_config):
  bstack1ll1l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡶࡸࡦࡸࡴ࠯ࠌࠣࠤࠧࠨࠢ⢛")
  if not bs_config:
    return {}
  bstack1lll111l11l1_opy_ = bstack11l1ll1ll_opy_(bs_config).bstack1lll111l1lll_opy_(bs_config)
  return bstack1lll111l11l1_opy_
def bstack1lll11ll1_opy_(bs_config, framework):
  bstack1lll11llll_opy_ = False
  bstack1ll1lllll_opy_ = False
  bstack1ll111lll111_opy_ = False
  if bstack1ll1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⢜") in bs_config:
    bstack1ll111lll111_opy_ = True
  elif bstack1ll1l11_opy_ (u"ࠩࡤࡴࡵ࠭⢝") in bs_config:
    bstack1lll11llll_opy_ = True
  else:
    bstack1ll1lllll_opy_ = True
  bstack11l1l111ll_opy_ = {
    bstack1ll1l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⢞"): bstack11l1l1l1_opy_.bstack1ll111lllll1_opy_(bs_config, framework),
    bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⢟"): a11y.is_enabled_root(bs_config),
    bstack1ll1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⢠"): bs_config.get(bstack1ll1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⢡"), False),
    bstack1ll1l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ⢢"): bstack1ll1lllll_opy_,
    bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⢣"): bstack1lll11llll_opy_,
    bstack1ll1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭⢤"): bstack1ll111lll111_opy_
  }
  return bstack11l1l111ll_opy_
@error_handler(class_method=False)
def bstack1ll111llll11_opy_(bs_config):
  try:
    bstack1ll111ll1lll_opy_ = json.loads(os.getenv(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ⢥"), bstack1ll1l11_opy_ (u"ࠫࢀࢃࠧ⢦")))
    bstack1ll111ll1lll_opy_ = bstack1ll11l111111_opy_(bs_config, bstack1ll111ll1lll_opy_)
    return {
        bstack1ll1l11_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧ⢧"): bstack1ll111ll1lll_opy_
    }
  except Exception as error:
    logger.error(bstack1ll1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ⢨").format(str(error)))
    return {}
def bstack1ll11l111111_opy_(bs_config, bstack1ll111ll1lll_opy_):
  if ((bstack1ll1l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⢩") in bs_config or not bstack111l1lll1l_opy_(bs_config)) and a11y.is_enabled_root(bs_config)):
    bstack1ll111ll1lll_opy_[bstack1ll1l11_opy_ (u"ࠣ࡫ࡱࡧࡱࡻࡤࡦࡇࡱࡧࡴࡪࡥࡥࡇࡻࡸࡪࡴࡳࡪࡱࡱࠦ⢪")] = True
  return bstack1ll111ll1lll_opy_
def bstack1ll11l11l11l_opy_(array, bstack1ll111lll11l_opy_, bstack1ll111llllll_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll111lll11l_opy_]
    result[key] = o[bstack1ll111llllll_opy_]
  return result
def bstack1ll11l111l1l_opy_(bstack11l1l1lll1_opy_=bstack1ll1l11_opy_ (u"ࠩࠪ⢫")):
  bstack1ll111lll1ll_opy_ = a11y.on()
  bstack1ll111llll1l_opy_ = bstack11l1l1l1_opy_.on()
  bstack1ll11l1111l1_opy_ = percy.bstack1111ll1l1l_opy_()
  if bstack1ll11l1111l1_opy_ and not bstack1ll111llll1l_opy_ and not bstack1ll111lll1ll_opy_:
    return bstack11l1l1lll1_opy_ not in [bstack1ll1l11_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ⢬"), bstack1ll1l11_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⢭")]
  elif bstack1ll111lll1ll_opy_ and not bstack1ll111llll1l_opy_:
    return bstack11l1l1lll1_opy_ not in [bstack1ll1l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⢮"), bstack1ll1l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⢯"), bstack1ll1l11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⢰")]
  return bstack1ll111lll1ll_opy_ or bstack1ll111llll1l_opy_ or bstack1ll11l1111l1_opy_
@error_handler(class_method=False)
def bstack1ll11l11ll1l_opy_(bstack11l1l1lll1_opy_, test=None):
  bstack1ll11l11111l_opy_ = a11y.on()
  if not bstack1ll11l11111l_opy_ or bstack11l1l1lll1_opy_ not in [bstack1ll1l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⢱"), bstack1ll1l11_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⢲"), bstack1ll1l11_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ⢳")] or test == None:
    return None
  return {
    bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⢴"): bstack1ll11l11111l_opy_ and bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ⢵"), None) == True and a11y.is_enabled_testcase(test.get(bstack1ll1l11_opy_ (u"࠭ࡴࡢࡩࡶࠫ⢶"), []))
  }
def bstack1ll111lll1l1_opy_(bs_config, framework):
  bstack1lll11llll_opy_ = False
  bstack1ll1lllll_opy_ = False
  bstack1ll111lll111_opy_ = False
  if bstack1ll1l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⢷") in bs_config:
    bstack1ll111lll111_opy_ = True
  elif bstack1ll1l11_opy_ (u"ࠨࡣࡳࡴࠬ⢸") in bs_config:
    bstack1lll11llll_opy_ = True
  else:
    bstack1ll1lllll_opy_ = True
  bstack11l1l111ll_opy_ = {
    bstack1ll1l11_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⢹"): bstack11l1l1l1_opy_.bstack1ll111lllll1_opy_(bs_config, framework),
    bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⢺"): a11y.bstack1l111l111_opy_(bs_config),
    bstack1ll1l11_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⢻"): bs_config.get(bstack1ll1l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⢼"), False),
    bstack1ll1l11_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⢽"): bstack1ll1lllll_opy_,
    bstack1ll1l11_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⢾"): bstack1lll11llll_opy_,
    bstack1ll1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ⢿"): bstack1ll111lll111_opy_
  }
  return bstack11l1l111ll_opy_